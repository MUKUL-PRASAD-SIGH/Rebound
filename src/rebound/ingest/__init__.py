"""Razorpay-shaped ingest, signed webhook validation, and MVP-mode reconciliation."""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from rebound.audit import append_audit
from rebound.config import get_settings
from rebound.db.models import ActionAttempt, Case, Outcome, RazorpayWebhookEvent
from rebound.schemas.enums import Action, AuditKind, CaseSource, CaseStatus, OutcomeLabel, OutcomeResult
from rebound.security import pseudonymize_customer_ref, redact_sensitive


class IngestValidationError(ValueError):
    pass


@dataclass(frozen=True)
class WebhookProcessResult:
    case: Case
    created: bool
    reconciled: bool
    event_type: str


def verify_razorpay_webhook_signature(
    raw_body: bytes,
    signature: str | None,
    webhook_secret: str,
) -> bool:
    """Verify Razorpay's HMAC-SHA256 signature against the unchanged raw body."""
    if not webhook_secret:
        return True
    if not signature:
        return False
    expected = hmac.new(
        webhook_secret.encode("utf-8"), raw_body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def _entity(payload: dict[str, Any], resource: str) -> dict[str, Any]:
    value = payload.get("payload", {}).get(resource, {}).get("entity", {})
    return value if isinstance(value, dict) else {}


def _payment_link_attempt(
    db: Session,
    payload: dict[str, Any],
) -> ActionAttempt | None:
    """Find the original Rebound attempt from link ID, then from Rebound's note."""
    link = _entity(payload, "payment_link")
    link_id = link.get("id")
    if isinstance(link_id, str) and link_id:
        attempt = db.scalar(
            select(ActionAttempt)
            .where(ActionAttempt.razorpay_payment_link_id == link_id)
            .order_by(ActionAttempt.created_at.desc())
        )
        if attempt:
            return attempt

    notes = link.get("notes")
    case_id = notes.get("rebound_case_id") if isinstance(notes, dict) else None
    if not isinstance(case_id, str) or not case_id:
        return None
    return db.scalar(
        select(ActionAttempt)
        .where(
            ActionAttempt.case_id == case_id,
            ActionAttempt.action == Action.PAYMENT_LINK.value,
            ActionAttempt.mode == "mvp_mode",
        )
        .order_by(ActionAttempt.created_at.desc())
    )


def reconcile_payment_link_state(
    db: Session,
    link: dict[str, Any],
    *,
    source: str,
    event_id: str | None = None,
) -> Case | None:
    """Apply an authoritative Razorpay Payment Link terminal state to its case."""
    status = str(link.get("status") or "")
    if status not in {"paid", "expired", "cancelled"}:
        return None
    attempt = _payment_link_attempt(
        db,
        {"payload": {"payment_link": {"entity": link}}},
    )
    if not attempt:
        return None
    case = db.get(Case, attempt.case_id)
    if not case:
        return None

    outcome = db.scalar(
        select(Outcome)
        .where(
            Outcome.action_attempt_id == attempt.id,
            Outcome.label == OutcomeLabel.MVP_MODE.value,
        )
        .order_by(Outcome.observed_at.desc())
    )
    if outcome is None:
        outcome = Outcome(
            case_id=case.id,
            action_attempt_id=attempt.id,
            result=OutcomeResult.PENDING.value,
            value_paise=0,
            label=OutcomeLabel.MVP_MODE.value,
        )
        db.add(outcome)

    if status == "paid":
        value = int(link.get("amount_paid") or link.get("amount") or case.amount_paise)
        outcome.result = OutcomeResult.RECOVERED.value
        outcome.value_paise = value
        case.status = CaseStatus.RECOVERED.value
    else:
        outcome.result = OutcomeResult.FAILED.value
        outcome.value_paise = 0
        case.status = CaseStatus.OPEN.value

    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.OUTCOME,
        {
            "source": source,
            "event_id": event_id,
            "event_type": f"payment_link.{status}",
            "result": outcome.result,
            "value_paise": outcome.value_paise,
            "label": OutcomeLabel.MVP_MODE.value,
            "attempt_id": attempt.id,
            "case_status": case.status,
        },
    )
    return case


def upsert_from_webhook_payload(
    db: Session,
    payload: dict[str, Any],
    *,
    event_id: str | None = None,
) -> tuple[Case, bool]:
    """Upsert a payment/subscription-shaped failure payload or the flat demo shape."""
    if not isinstance(payload, dict) or not payload:
        raise IngestValidationError("empty_or_invalid_payload")

    external_event_id = event_id or payload.get("id") or payload.get("event_id")
    entity = (
        _entity(payload, "payment")
        or _entity(payload, "subscription")
        or payload.get("entity")
        or payload
    )
    if not isinstance(entity, dict):
        entity = {}

    case_key = (
        payload.get("case_key")
        or (f"wh-{external_event_id}" if external_event_id else None)
        or (f"wh-{entity['id']}" if entity.get("id") else None)
    )
    if not case_key:
        raise IngestValidationError("missing_case_key_or_event_id")

    if external_event_id:
        existing = db.scalar(select(Case).where(Case.external_event_id == str(external_event_id)))
        if existing:
            return existing, False

    existing_key = db.scalar(select(Case).where(Case.case_key == case_key))
    if existing_key:
        return existing_key, False

    amount = int(
        entity.get("amount")
        or entity.get("amount_paise")
        or payload.get("amount_paise")
        or 0
    )
    if amount <= 0:
        raise IngestValidationError("amount_paise_required_positive")

    customer_ref = str(
        entity.get("customer_id")
        or entity.get("email")
        or payload.get("customer_ref")
        or ""
    ).strip()
    if not customer_ref or customer_ref == "unknown":
        raise IngestValidationError("customer_ref_required")

    case = Case(
        case_key=case_key,
        source=CaseSource.WEBHOOK.value,
        external_event_id=str(external_event_id) if external_event_id else None,
        status=CaseStatus.OPEN.value,
        amount_paise=amount,
        currency=entity.get("currency") or "INR",
        # Customer references are pseudonymised before they reach the local DB.
        customer_ref=pseudonymize_customer_ref(
            customer_ref,
            salt=get_settings().rebound_pii_hash_salt,
        ),
        failure_code=entity.get("error_code") or payload.get("failure_code"),
        failure_class=payload.get("failure_class")
        or entity.get("error_reason")
        or "unknown",
        attempt_n=int(payload.get("attempt_n") or 1),
        tenure_days=int(payload.get("tenure_days") or 30),
        method=str(entity.get("method") or payload.get("method") or "upi"),
        payload_json=json.dumps(redact_sensitive(payload)),
    )
    db.add(case)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.INGESTED,
        {"source": "webhook", "event_id": external_event_id, "case_key": case_key},
    )
    return case, True


def process_razorpay_webhook(
    db: Session,
    payload: dict[str, Any],
    *,
    event_id: str | None = None,
) -> WebhookProcessResult:
    """Idempotently reconcile a Rebound Payment Link or ingest a new failure event."""
    event_type = str(payload.get("event") or "unknown")
    if event_id:
        delivered = db.scalar(
            select(RazorpayWebhookEvent).where(RazorpayWebhookEvent.external_event_id == event_id)
        )
        if delivered and delivered.case_id:
            case = db.get(Case, delivered.case_id)
            if case:
                return WebhookProcessResult(case, created=False, reconciled=False, event_type=event_type)

    if event_type in {"payment_link.paid", "payment_link.expired", "payment_link.cancelled"}:
        link = dict(_entity(payload, "payment_link"))
        link["status"] = event_type.removeprefix("payment_link.")
        case = reconcile_payment_link_state(
            db,
            link,
            source="razorpay_webhook",
            event_id=event_id,
        )
    else:
        case = None
    reconciled = case is not None
    created = False
    if case is None:
        case, created = upsert_from_webhook_payload(db, payload, event_id=event_id)

    if event_id:
        db.add(
            RazorpayWebhookEvent(
                external_event_id=event_id,
                event_type=event_type,
                case_id=case.id,
                payload_json=json.dumps(redact_sensitive(payload)),
            )
        )
        db.flush()
    return WebhookProcessResult(case, created=created, reconciled=reconciled, event_type=event_type)

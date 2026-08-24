"""Webhook-shaped ingest (signature verify optional / stubbed)."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from rebound.audit import append_audit
from rebound.db.models import Case
from rebound.schemas.enums import AuditKind, CaseSource, CaseStatus


def upsert_from_webhook_payload(db: Session, payload: dict[str, Any]) -> tuple[Case, bool]:
    """
    Accept Razorpay-like JSON:
    { "event": "...", "payload": { "payment": { "entity": {...} } } }
    or a flat demo shape with case fields.
    Returns (case, created).
    """
    event_id = payload.get("id") or payload.get("event_id")
    entity = (
        payload.get("payload", {}).get("payment", {}).get("entity")
        or payload.get("payload", {}).get("subscription", {}).get("entity")
        or payload.get("entity")
        or payload
    )

    case_key = (
        payload.get("case_key")
        or (f"wh-{event_id}" if event_id else None)
        or f"wh-{entity.get('id', 'unknown')}"
    )

    if event_id:
        existing = db.scalar(select(Case).where(Case.external_event_id == str(event_id)))
        if existing:
            return existing, False

    existing_key = db.scalar(select(Case).where(Case.case_key == case_key))
    if existing_key:
        return existing_key, False

    amount = int(entity.get("amount") or entity.get("amount_paise") or payload.get("amount_paise") or 0)
    case = Case(
        case_key=case_key,
        source=CaseSource.WEBHOOK.value,
        external_event_id=str(event_id) if event_id else None,
        status=CaseStatus.OPEN.value,
        amount_paise=amount,
        currency=entity.get("currency") or "INR",
        customer_ref=str(entity.get("customer_id") or entity.get("email") or payload.get("customer_ref") or "unknown"),
        failure_code=entity.get("error_code") or payload.get("failure_code"),
        failure_class=payload.get("failure_class")
        or entity.get("error_reason")
        or "unknown",
        attempt_n=int(payload.get("attempt_n") or 1),
        tenure_days=int(payload.get("tenure_days") or 30),
        method=str(entity.get("method") or payload.get("method") or "upi"),
        payload_json=json.dumps(payload),
    )
    db.add(case)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.INGESTED,
        {"source": "webhook", "event_id": event_id, "case_key": case_key},
    )
    return case, True

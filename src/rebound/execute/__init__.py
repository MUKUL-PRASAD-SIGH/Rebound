"""Executors: dry-run, simulated outreach, and Razorpay test-mode Payment Links."""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from typing import Any

import httpx

from rebound.config import get_settings
from rebound.schemas.enums import Action, ExecutionMode


PAYMENT_LINKS_URL = "https://api.razorpay.com/v1/payment_links"
PAYMENT_LINK_TIMEOUT_SECONDS = 10.0


@dataclass
class ExecuteResult:
    mode: str
    request: dict[str, Any]
    response: dict[str, Any]
    razorpay_payment_link_id: str | None = None


class PaymentLinkExecutionError(RuntimeError):
    """Raised when a configured Razorpay test-mode request cannot be completed safely."""


class PaymentLinkConfigurationError(ValueError):
    """Raised when a supposedly test-mode request is configured with unsafe credentials."""


def _is_razorpay_test_key(key_id: str) -> bool:
    """Razorpay test key IDs begin with ``rzp_test_``; live keys must never execute here."""
    return key_id.startswith("rzp_test_")


def _payment_link_reference(case_id: str, decision_id: str) -> str:
    """Create a deterministic, Razorpay-compatible reference (maximum 40 characters)."""
    digest = hashlib.sha256(f"{case_id}:{decision_id}".encode("utf-8")).hexdigest()
    return f"rbnd_{digest[:35]}"


def _existing_payment_link(
    reference_id: str,
    auth: tuple[str, str],
) -> dict[str, Any] | None:
    """Look up an already-created link after an ambiguous create failure."""
    try:
        response = httpx.get(
            PAYMENT_LINKS_URL,
            params={"reference_id": reference_id},
            auth=auth,
            timeout=PAYMENT_LINK_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError):
        return None

    links = payload.get("payment_links", [])
    if not isinstance(links, list):
        return None
    for link in links:
        if isinstance(link, dict) and link.get("reference_id") == reference_id:
            return link
    return None


def _result_from_payment_link(
    link: dict[str, Any],
    request_payload: dict[str, Any],
    *,
    reconciled: bool = False,
) -> ExecuteResult:
    link_id = link.get("id")
    short_url = link.get("short_url")
    if not isinstance(link_id, str) or not isinstance(short_url, str):
        raise PaymentLinkExecutionError("razorpay_payment_link_response_invalid")
    return ExecuteResult(
        mode=ExecutionMode.LIVE_TEST.value,
        request=request_payload,
        response={
            "ok": True,
            "payment_link_id": link_id,
            "url": short_url,
            "status": link.get("status"),
            "reconciled_from_reference_lookup": reconciled,
        },
        razorpay_payment_link_id=link_id,
    )


def _create_razorpay_payment_link(
    *,
    case_id: str,
    case_key: str,
    decision_id: str,
    amount_paise: int,
    currency: str,
    key_id: str,
    key_secret: str,
) -> ExecuteResult:
    if amount_paise <= 0:
        raise PaymentLinkExecutionError("razorpay_payment_link_amount_invalid")

    reference_id = _payment_link_reference(case_id, decision_id)
    request_payload: dict[str, Any] = {
        "action": Action.PAYMENT_LINK.value,
        "amount": amount_paise,
        "currency": currency,
        "accept_partial": False,
        "reference_id": reference_id,
        "description": f"Rebound recovery {case_key}"[:2048],
        # Rebound deliberately does not send customer notifications itself.
        "notify": {"sms": False, "email": False},
        "reminder_enable": False,
        "notes": {
            "rebound_case_id": case_id,
            "rebound_decision_id": decision_id,
        },
    }
    auth = (key_id, key_secret)

    try:
        response = httpx.post(
            PAYMENT_LINKS_URL,
            json={key: value for key, value in request_payload.items() if key != "action"},
            auth=auth,
            timeout=PAYMENT_LINK_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return _result_from_payment_link(response.json(), request_payload)
    except (httpx.HTTPError, ValueError):
        # Razorpay rejects duplicate references, and a network timeout can occur after
        # it creates the link. Resolve by the deterministic reference before failing.
        existing = _existing_payment_link(reference_id, auth)
        if existing:
            return _result_from_payment_link(existing, request_payload, reconciled=True)
        raise PaymentLinkExecutionError("razorpay_payment_link_request_failed") from None


def execution_mode() -> str:
    return get_settings().rebound_execution_mode


def execute_action(
    action: Action,
    case_id: str,
    case_key: str,
    amount_paise: int,
    *,
    currency: str = "INR",
    decision_id: str | None = None,
) -> ExecuteResult:
    """
    Day 04: always safe.
    - stop / escalate → dry_run log
    - notify_update_method → simulated outreach
    - silent_retry / payment_link → dry_run unless explicitly configured for test_mode
    - payment_link in test_mode with both Razorpay test keys → live test Payment Link
    """
    settings = get_settings()
    mode = settings.rebound_execution_mode

    if action == Action.STOP:
        return ExecuteResult(
            mode=ExecutionMode.DRY_RUN.value,
            request={"action": action.value, "case_id": case_id},
            response={"ok": True, "detail": "stopped_no_side_effect"},
        )

    if action == Action.ESCALATE:
        return ExecuteResult(
            mode=ExecutionMode.DRY_RUN.value,
            request={"action": action.value, "case_id": case_id},
            response={"ok": True, "detail": "escalated_to_human_queue"},
        )

    if action == Action.NOTIFY_UPDATE_METHOD:
        return ExecuteResult(
            mode=ExecutionMode.SIMULATED.value,
            request={
                "action": action.value,
                "case_id": case_id,
                "channel": "email_or_whatsapp",
                "template": "update_payment_method",
            },
            response={
                "ok": True,
                "detail": "outreach_simulated_not_sent",
                "label": "simulated",
            },
        )

    # silent_retry or payment_link
    if mode == "test_mode" and action == Action.PAYMENT_LINK:
        if settings.razorpay_key_id and settings.razorpay_key_secret:
            if not _is_razorpay_test_key(settings.razorpay_key_id):
                raise PaymentLinkConfigurationError(
                    "razorpay_test_mode_requires_rzp_test_key"
                )
            return _create_razorpay_payment_link(
                case_id=case_id,
                case_key=case_key,
                decision_id=decision_id or case_id,
                amount_paise=amount_paise,
                currency=currency,
                key_id=settings.razorpay_key_id,
                key_secret=settings.razorpay_key_secret,
            )
        return ExecuteResult(
            mode=ExecutionMode.DRY_RUN.value,
            request={"action": action.value, "case_id": case_id, "amount_paise": amount_paise},
            response={
                "ok": True,
                "detail": "dry_run_payment_link_missing_razorpay_test_credentials",
                "would_create_payment_link": True,
            },
        )

    return ExecuteResult(
        mode=ExecutionMode.DRY_RUN.value,
        request={"action": action.value, "case_id": case_id, "amount_paise": amount_paise},
        response={
            "ok": True,
            "detail": f"dry_run_{action.value}",
            "would_create_payment_link": action == Action.PAYMENT_LINK,
        },
    )


def result_to_json(result: ExecuteResult) -> tuple[str, str]:
    return json.dumps(result.request), json.dumps(result.response)

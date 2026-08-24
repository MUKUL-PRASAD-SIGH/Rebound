"""Executors: dry_run / simulated / test_mode Payment Link (Day 04 dry_run + simulated)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from rebound.config import get_settings
from rebound.schemas.enums import Action, ExecutionMode


@dataclass
class ExecuteResult:
    mode: str
    request: dict[str, Any]
    response: dict[str, Any]
    razorpay_payment_link_id: str | None = None


def execution_mode() -> str:
    return get_settings().rebound_execution_mode


def execute_action(action: Action, case_id: str, case_key: str, amount_paise: int) -> ExecuteResult:
    """
    Day 04: always safe.
    - stop / escalate → dry_run log
    - notify_update_method → simulated outreach
    - silent_retry / payment_link → dry_run unless REBOUND_EXECUTION_MODE=test_mode
      (real Razorpay Payment Link wired when keys present; otherwise dry_run fallback)
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
    if mode == "test_mode" and action == Action.PAYMENT_LINK and settings.razorpay_key_id:
        # Placeholder for live test-mode SDK call — keys optional on Day 04
        link_id = f"plink_dry_{case_key}"
        return ExecuteResult(
            mode=ExecutionMode.DRY_RUN.value,
            request={
                "action": action.value,
                "amount_paise": amount_paise,
                "note": "test_mode_keys_present_but_http_call_deferred_safe_dry_run",
            },
            response={"ok": True, "payment_link_id": link_id, "url": f"https://rzp.io/i/{link_id}"},
            razorpay_payment_link_id=link_id,
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

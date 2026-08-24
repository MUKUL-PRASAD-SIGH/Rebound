"""Deterministic policy gate — allowlist + caps + confidence floor."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound.config import get_settings
from rebound.db.models import ActionAttempt, Case
from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import ALLOWLISTED_ACTIONS, Action, GateResult

MAX_SILENT_RETRIES = 3
MAX_NOTIFIES = 2
MIN_CONFIDENCE = 0.35


@dataclass
class GateDecision:
    action: Action
    gate_result: GateResult
    reason: str
    policy_version: str


def _count(db: Session, case_id: str, action: str) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(ActionAttempt)
            .where(ActionAttempt.case_id == case_id, ActionAttempt.action == action)
        )
        or 0
    )


def gate(proposal: ProposalPayload, db: Session | None = None, case: Case | None = None) -> GateDecision:
    settings = get_settings()
    version = settings.policy_version

    if proposal.action.value not in ALLOWLISTED_ACTIONS:
        return GateDecision(
            action=Action.STOP,
            gate_result=GateResult.REJECT,
            reason="reject_unknown_action",
            policy_version=version,
        )

    if proposal.action != Action.STOP and proposal.confidence < MIN_CONFIDENCE:
        return GateDecision(
            action=Action.STOP,
            gate_result=GateResult.REWRITE_STOP,
            reason=f"confidence_below_{MIN_CONFIDENCE}",
            policy_version=version,
        )

    if db is not None and case is not None:
        if proposal.action == Action.SILENT_RETRY and _count(db, case.id, Action.SILENT_RETRY.value) >= MAX_SILENT_RETRIES:
            return GateDecision(
                action=Action.STOP,
                gate_result=GateResult.REWRITE_STOP,
                reason="max_silent_retries_exceeded",
                policy_version=version,
            )
        if proposal.action == Action.NOTIFY_UPDATE_METHOD and _count(
            db, case.id, Action.NOTIFY_UPDATE_METHOD.value
        ) >= MAX_NOTIFIES:
            return GateDecision(
                action=Action.STOP,
                gate_result=GateResult.REWRITE_STOP,
                reason="max_notifies_exceeded",
                policy_version=version,
            )
        if (
            case.amount_paise >= 500_000
            and proposal.confidence < 0.5
            and proposal.action not in {Action.ESCALATE, Action.STOP}
        ):
            return GateDecision(
                action=Action.ESCALATE,
                gate_result=GateResult.REWRITE_ESCALATE,
                reason="high_value_low_confidence_escalate",
                policy_version=version,
            )

    return GateDecision(
        action=proposal.action,
        gate_result=GateResult.ALLOW,
        reason="policy_allow",
        policy_version=version,
    )

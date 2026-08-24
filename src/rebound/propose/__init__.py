"""Rules-based proposers for Day 04 happy path (EV models land Day 05)."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound.db.models import ActionAttempt, Case
from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import Action, ProposerKind


def _count_actions(db: Session, case_id: str, action: str) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(ActionAttempt)
            .where(ActionAttempt.case_id == case_id, ActionAttempt.action == action)
        )
        or 0
    )


def propose_rules_ladder(db: Session, case: Case) -> ProposalPayload:
    """
    Day-04 deterministic ladder (similar shape to Baseline A).
    Full EV scorer extends this on Day 05.
    """
    n_retry = _count_actions(db, case.id, Action.SILENT_RETRY.value)
    n_link = _count_actions(db, case.id, Action.PAYMENT_LINK.value)
    n_notify = _count_actions(db, case.id, Action.NOTIFY_UPDATE_METHOD.value)

    if case.amount_paise >= 500_000 and case.failure_class == "unknown":
        return ProposalPayload(
            action=Action.ESCALATE,
            confidence=0.55,
            p_recover=0.4,
            ev=float(case.amount_paise) * 0.4 - 100,
            rationale="high_value_unknown_failure_escalate",
        )

    if case.attempt_n <= 2 and n_retry < 2:
        return ProposalPayload(
            action=Action.SILENT_RETRY,
            confidence=0.7,
            p_recover=0.45,
            ev=float(case.amount_paise) * 0.45 - 50,
            rationale=f"rules_ladder_retry attempt_n={case.attempt_n} prior_retries={n_retry}",
        )

    if n_link < 1:
        return ProposalPayload(
            action=Action.PAYMENT_LINK,
            confidence=0.65,
            p_recover=0.35,
            ev=float(case.amount_paise) * 0.35 - 200,
            rationale="rules_ladder_payment_link",
        )

    if case.failure_class in {"expired_card", "insufficient_funds"} and n_notify < 1:
        return ProposalPayload(
            action=Action.NOTIFY_UPDATE_METHOD,
            confidence=0.6,
            p_recover=0.3,
            ev=float(case.amount_paise) * 0.3 - 300,
            rationale="rules_ladder_notify_update_method",
        )

    return ProposalPayload(
        action=Action.STOP,
        confidence=0.8,
        p_recover=0.05,
        ev=0.0,
        rationale="rules_ladder_stop_exhausted",
    )


def propose_for_case(db: Session, case: Case) -> tuple[ProposalPayload, ProposerKind]:
    return propose_rules_ladder(db, case), ProposerKind.RULES

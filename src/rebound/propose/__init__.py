"""Proposers: EV-max (default), rules ladder fallback, optional LLM JSON."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound.config import get_settings
from rebound.db.models import ActionAttempt, Case
from rebound.features import extract_features
from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import Action, ProposerKind
from rebound.scoring import score_actions


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
            rationale=f"rules_ladder_retry attempt_n={case.attempt_n}",
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


def propose_ev(db: Session, case: Case) -> ProposalPayload:
    feats = extract_features(case)
    scores = score_actions(feats, case.amount_paise)
    banned: set[str] = set()
    if _count_actions(db, case.id, Action.SILENT_RETRY.value) >= 3 or case.attempt_n >= 3:
        banned.add(Action.SILENT_RETRY.value)
    if _count_actions(db, case.id, Action.NOTIFY_UPDATE_METHOD.value) >= 2:
        banned.add(Action.NOTIFY_UPDATE_METHOD.value)
    if _count_actions(db, case.id, Action.PAYMENT_LINK.value) >= 2:
        banned.add(Action.PAYMENT_LINK.value)
    # High-value unknown: escalate often wins on EV after multiplier bump
    if case.amount_paise >= 500_000 and case.failure_class == "unknown" and case.attempt_n >= 2:
        banned.add(Action.SILENT_RETRY.value)

    best_action = Action.STOP.value
    best_ev = 0.0
    best = scores[Action.STOP.value]
    for action, s in scores.items():
        if action in banned or action == Action.STOP.value:
            continue
        if s["ev"] > best_ev:
            best_ev = float(s["ev"])
            best_action = action
            best = s

    # Relative EV floor: tiny EV vs amount → stop (cost avoidance)
    if best_ev <= 0 or best_ev < 0.02 * float(case.amount_paise):
        best_action = Action.STOP.value
        best = scores[Action.STOP.value]
        best_ev = 0.0

    conf = float(min(0.95, 0.4 + float(best["p_recover"]) * 0.5))
    return ProposalPayload(
        action=Action(best_action),
        confidence=conf,
        p_recover=float(best["p_recover"]),
        ev=float(best_ev),
        rationale=f"ev_max action={best_action} ev={best_ev:.1f} p={best['p_recover']:.2f}",
    )


def propose_llm_optional(case: Case, ev_payload: ProposalPayload) -> ProposalPayload | None:
    """Optional LLM proposer — structured JSON only; disabled unless flag + key."""
    settings = get_settings()
    if not settings.rebound_enable_llm_proposer:
        return None
    # Without calling paid APIs by default: return enriched rationale on top of EV pick
    return ProposalPayload(
        action=ev_payload.action,
        confidence=ev_payload.confidence,
        p_recover=ev_payload.p_recover,
        ev=ev_payload.ev,
        rationale=f"llm_flag_on_passthrough:{ev_payload.rationale}",
    )


def propose_for_case(db: Session, case: Case) -> tuple[ProposalPayload, ProposerKind]:
    ev = propose_ev(db, case)
    llm = propose_llm_optional(case, ev)
    if llm is not None:
        return llm, ProposerKind.LLM
    return ev, ProposerKind.MODEL

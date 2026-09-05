"""Proposers: EV-max (default), rules ladder fallback, optional LLM JSON."""

from __future__ import annotations

import json
from typing import Any

import httpx
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound.config import get_settings
from rebound.db.models import ActionAttempt, Case
from rebound.features import extract_features
from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import Action, ProposerKind
from rebound.scoring import score_actions


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_TIMEOUT_SECONDS = 10.0
LLM_RATIONALE_MAX_CHARS = 360


def _count_actions(db: Session, case_id: str, action: str) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(ActionAttempt)
            .where(ActionAttempt.case_id == case_id, ActionAttempt.action == action)
        )
        or 0
    )


def _banned_actions(db: Session | None, case: Case, *, ignore_history: bool) -> set[str]:
    """Return actions excluded by Rebound's deterministic proposal constraints."""
    banned: set[str] = set()
    retry_n = 0 if ignore_history or db is None else _count_actions(db, case.id, Action.SILENT_RETRY.value)
    notify_n = (
        0 if ignore_history or db is None else _count_actions(db, case.id, Action.NOTIFY_UPDATE_METHOD.value)
    )
    link_n = 0 if ignore_history or db is None else _count_actions(db, case.id, Action.PAYMENT_LINK.value)

    if retry_n >= 3 or case.attempt_n >= 3:
        banned.add(Action.SILENT_RETRY.value)
    if notify_n >= 2:
        banned.add(Action.NOTIFY_UPDATE_METHOD.value)
    if link_n >= 2:
        banned.add(Action.PAYMENT_LINK.value)
    if case.amount_paise >= 500_000 and case.failure_class == "unknown" and case.attempt_n >= 2:
        banned.add(Action.SILENT_RETRY.value)
    return banned


def _proposal_from_scored_action(
    action: Action,
    scores: dict[str, dict[str, Any]],
    rationale: str,
) -> ProposalPayload:
    """Use deterministic recovery and EV metrics for every proposed action."""
    score = scores[action.value]
    p_recover = float(score["p_recover"])
    confidence = float(min(0.95, 0.4 + p_recover * 0.5))
    return ProposalPayload(
        action=action,
        confidence=confidence,
        p_recover=p_recover,
        ev=float(score["ev"]),
        rationale=rationale,
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


def propose_ev(
    db: Session | None,
    case: Case,
    *,
    ignore_history: bool = False,
) -> ProposalPayload:
    """EV-max propose. Set ignore_history=True for batch eval (fair vs baselines)."""
    feats = extract_features(case)
    scores = score_actions(feats, case.amount_paise)
    banned = _banned_actions(db, case, ignore_history=ignore_history)

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

    if best_ev <= 0 or best_ev < 0.02 * float(case.amount_paise):
        best_action = Action.STOP.value
        best = scores[Action.STOP.value]
        best_ev = 0.0

    return _proposal_from_scored_action(
        Action(best_action),
        scores,
        rationale=f"ev_max action={best_action} ev={best_ev:.1f} p={best['p_recover']:.2f}",
    )


def _llm_candidate_actions(
    db: Session,
    case: Case,
    scores: dict[str, dict[str, Any]],
) -> list[Action]:
    """Restrict the model to viable, non-exhausted actions plus the safe STOP option."""
    banned = _banned_actions(db, case, ignore_history=False)
    min_ev = 0.02 * float(case.amount_paise)
    candidates = [Action.STOP]
    for action in Action:
        if action == Action.STOP or action.value in banned:
            continue
        if float(scores[action.value]["ev"]) >= min_ev:
            candidates.append(action)
    return candidates


def _openai_llm_proposal(
    *,
    case: Case,
    candidates: list[Action],
    scores: dict[str, dict[str, Any]],
    api_key: str,
    model: str,
) -> tuple[Action, str] | None:
    """Request a bounded action choice from OpenAI's Responses API.

    The request intentionally excludes IDs, customer references, and raw payment payloads.
    It has no tools and returns only a schema-constrained action and short rationale.
    """
    allowed_actions = [action.value for action in candidates]
    request_payload = {
        "model": model,
        "store": False,
        "max_output_tokens": 180,
        "instructions": (
            "You are a bounded recovery-action proposer. Choose exactly one action from the "
            "provided candidates using only the supplied non-identifying case signals and "
            "deterministic action metrics. You cannot execute payments, change policy, request "
            "more data, or propose an action outside the candidates. Return a concise rationale "
            "without personal data."
        ),
        "input": json.dumps(
            {
                "case": {
                    "amount_paise": case.amount_paise,
                    "currency": case.currency,
                    "failure_class": case.failure_class,
                    "attempt_n": case.attempt_n,
                    "tenure_days": case.tenure_days,
                    "method": case.method,
                },
                "candidates": [
                    {
                        "action": action.value,
                        "p_recover": round(float(scores[action.value]["p_recover"]), 4),
                        "expected_value_paise": round(float(scores[action.value]["ev"]), 2),
                    }
                    for action in candidates
                ],
            }
        ),
        "text": {
            "format": {
                "type": "json_schema",
                "name": "recovery_action_proposal",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "action": {"type": "string", "enum": allowed_actions},
                        "rationale": {"type": "string", "maxLength": LLM_RATIONALE_MAX_CHARS},
                    },
                    "required": ["action", "rationale"],
                },
            }
        },
    }
    try:
        response = httpx.post(
            OPENAI_RESPONSES_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=request_payload,
            timeout=OPENAI_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        if result.get("status") != "completed":
            return None
        output_text = result.get("output_text")
        if not isinstance(output_text, str):
            return None
        output = json.loads(output_text)
        action = Action(output["action"])
        rationale = " ".join(str(output["rationale"]).split())[:LLM_RATIONALE_MAX_CHARS]
    except (httpx.HTTPError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None

    if action not in candidates or not rationale:
        return None
    return action, rationale


def propose_llm_optional(
    db: Session,
    case: Case,
    ev_payload: ProposalPayload,
) -> ProposalPayload | None:
    """Optionally let an LLM choose among deterministic, policy-safe candidates.

    Disabled, missing-key, malformed-output, and network-error paths all fall back to
    the default EV proposer. The caller always sends the result through ``gate``.
    """
    settings = get_settings()
    if not settings.rebound_enable_llm_proposer or not settings.openai_api_key:
        return None

    scores = score_actions(extract_features(case), case.amount_paise)
    candidates = _llm_candidate_actions(db, case, scores)
    if candidates == [Action.STOP]:
        return None

    selected = _openai_llm_proposal(
        case=case,
        candidates=candidates,
        scores=scores,
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    if selected is None:
        return None
    action, rationale = selected
    return _proposal_from_scored_action(
        action,
        scores,
        rationale=(
            f"llm_openai_selected action={action.value}; {rationale}; "
            f"ev_baseline={ev_payload.action.value}"
        ),
    )


def propose_for_case(db: Session, case: Case) -> tuple[ProposalPayload, ProposerKind]:
    ev = propose_ev(db, case)
    llm = propose_llm_optional(db, case, ev)
    if llm is not None:
        return llm, ProposerKind.LLM
    return ev, ProposerKind.MODEL

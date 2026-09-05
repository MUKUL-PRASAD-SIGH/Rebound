"""Decide → gate → (optional) execute → simulated outcome orchestration."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from rebound.audit import append_audit
from rebound.db.models import ActionAttempt, Case, Decision, Outcome, Proposal
from rebound.execute import execute_action, result_to_json
from rebound.features import extract_features
from rebound.policy import gate
from rebound.propose import propose_for_case
from rebound.schemas.enums import Action, AuditKind, CaseStatus, ExecutionMode, OutcomeLabel, OutcomeResult
from rebound.scoring import score_actions

MAX_ATTEMPTS_BEFORE_FORCE_STOP = 4


@dataclass
class DecideResult:
    case_id: str
    proposal_id: str
    decision_id: str
    proposed_action: str
    gated_action: str
    gate_result: str
    gate_reason: str
    rationale: str
    confidence: float
    ev: float
    executed: bool = False
    attempt_id: str | None = None
    outcome: str | None = None


def decide_case(db: Session, case: Case, *, auto_execute: bool = False) -> DecideResult:
    features = extract_features(case)
    scores = score_actions(features, case.amount_paise)
    append_audit(
        db,
        case.id,
        AuditKind.SCORED,
        {
            "features": features,
            "action_ev": {a: {"ev": s["ev"], "p": s["p_recover"]} for a, s in scores.items()},
        },
    )

    payload, proposer_kind = propose_for_case(db, case)
    proposal = Proposal(
        case_id=case.id,
        action=payload.action.value,
        confidence=payload.confidence,
        ev=payload.ev,
        p_recover=payload.p_recover,
        rationale=payload.rationale,
        proposer=proposer_kind.value,
    )
    db.add(proposal)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.PROPOSED,
        {
            "action": payload.action.value,
            "confidence": payload.confidence,
            "ev": payload.ev,
            "p_recover": payload.p_recover,
            "rationale": payload.rationale,
            "proposer": proposer_kind.value,
        },
    )

    gated = gate(payload, db=db, case=case)
    decision = Decision(
        case_id=case.id,
        proposal_id=proposal.id,
        action=gated.action.value,
        gate_result=gated.gate_result.value,
        gate_reason=gated.reason,
        policy_version=gated.policy_version,
    )
    db.add(decision)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.GATED,
        {
            "gate_result": gated.gate_result.value,
            "action": gated.action.value,
            "reason": gated.reason,
            "policy_version": gated.policy_version,
        },
    )

    if gated.action == Action.STOP:
        case.status = CaseStatus.STOPPED.value
    elif gated.action == Action.ESCALATE:
        case.status = CaseStatus.ESCALATED.value
    else:
        case.status = CaseStatus.ACTING.value

    result = DecideResult(
        case_id=case.id,
        proposal_id=proposal.id,
        decision_id=decision.id,
        proposed_action=payload.action.value,
        gated_action=gated.action.value,
        gate_result=gated.gate_result.value,
        gate_reason=gated.reason,
        rationale=payload.rationale,
        confidence=payload.confidence,
        ev=payload.ev,
    )

    if auto_execute:
        attempt, outcome = _execute(db, case, decision, gated.action, p_recover=payload.p_recover)
        result.executed = True
        result.attempt_id = attempt.id
        result.outcome = outcome

    db.commit()
    return result


def execute_latest_decision(db: Session, case: Case) -> ActionAttempt:
    decision = db.scalar(
        select(Decision).where(Decision.case_id == case.id).order_by(Decision.created_at.desc())
    )
    if not decision:
        raise ValueError("no_decision")
    proposal = db.get(Proposal, decision.proposal_id) if decision.proposal_id else None
    p_recover = float(proposal.p_recover) if proposal else 0.2
    action = Action(decision.action)
    attempt, _ = _execute(db, case, decision, action, p_recover=p_recover)
    db.commit()
    return attempt


def _deterministic_uniform(case_id: str, attempt_id: str) -> float:
    digest = hashlib.sha256(f"{case_id}:{attempt_id}".encode()).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _record_outcome(
    db: Session,
    case: Case,
    attempt: ActionAttempt,
    action: Action,
    p_recover: float,
    execution_mode: str,
) -> str:
    # A real Razorpay Test Mode Payment Link must wait for its authoritative
    # signed webhook. Never simulate payment success after merely creating a link.
    if execution_mode == ExecutionMode.MVP_MODE.value and action == Action.PAYMENT_LINK:
        result = OutcomeResult.PENDING.value
        value = 0
        label = OutcomeLabel.MVP_MODE.value
        case.status = CaseStatus.ACTING.value
    elif action == Action.STOP:
        result = OutcomeResult.STOPPED.value
        value = 0
        label = OutcomeLabel.SIMULATED.value
        case.status = CaseStatus.STOPPED.value
    elif action == Action.ESCALATE:
        result = OutcomeResult.PENDING.value
        value = 0
        label = OutcomeLabel.SIMULATED.value
        case.status = CaseStatus.ESCALATED.value
    else:
        label = OutcomeLabel.SIMULATED.value
        u = _deterministic_uniform(case.id, attempt.id)
        if u < max(0.0, min(0.95, p_recover)):
            result = OutcomeResult.RECOVERED.value
            value = case.amount_paise
            case.status = CaseStatus.RECOVERED.value
        else:
            result = OutcomeResult.FAILED.value
            value = 0
            # Re-open for another decide step until attempt cap
            if case.attempt_n < MAX_ATTEMPTS_BEFORE_FORCE_STOP:
                case.attempt_n = int(case.attempt_n) + 1
                case.status = CaseStatus.OPEN.value
            else:
                case.status = CaseStatus.STOPPED.value
                result = OutcomeResult.STOPPED.value

    outcome = Outcome(
        case_id=case.id,
        action_attempt_id=attempt.id,
        result=result,
        value_paise=value,
        label=label,
    )
    db.add(outcome)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.OUTCOME,
        {
            "result": result,
            "value_paise": value,
            "label": label,
            "attempt_id": attempt.id,
            "case_status": case.status,
        },
    )
    return result


def _execute(
    db: Session,
    case: Case,
    decision: Decision,
    action: Action,
    *,
    p_recover: float,
) -> tuple[ActionAttempt, str | None]:
    idem = f"{case.id}:{action.value}:{decision.id}"
    existing = db.scalar(select(ActionAttempt).where(ActionAttempt.idempotency_key == idem))
    if existing:
        return existing, None

    exec_result = execute_action(
        action,
        case.id,
        case.case_key,
        case.amount_paise,
        currency=case.currency,
        decision_id=decision.id,
    )
    req_json, resp_json = result_to_json(exec_result)
    attempt = ActionAttempt(
        case_id=case.id,
        decision_id=decision.id,
        action=action.value,
        mode=exec_result.mode,
        request_json=req_json,
        response_json=resp_json,
        razorpay_payment_link_id=exec_result.razorpay_payment_link_id,
        idempotency_key=idem,
    )
    db.add(attempt)
    db.flush()
    append_audit(
        db,
        case.id,
        AuditKind.EXECUTED,
        {
            "action": action.value,
            "mode": exec_result.mode,
            "response": exec_result.response,
            "attempt_id": attempt.id,
        },
    )

    outcome = _record_outcome(db, case, attempt, action, p_recover, exec_result.mode)
    return attempt, outcome

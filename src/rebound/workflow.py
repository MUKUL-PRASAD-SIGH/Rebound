"""Decide → gate → (optional) execute orchestration for a single case."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from rebound.audit import append_audit
from rebound.db.models import ActionAttempt, Case, Decision, Proposal
from rebound.execute import execute_action, result_to_json
from rebound.features import extract_features
from rebound.policy import gate
from rebound.propose import propose_for_case
from rebound.schemas.enums import Action, AuditKind, CaseStatus


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


def decide_case(db: Session, case: Case, *, auto_execute: bool = False) -> DecideResult:
    features = extract_features(case)
    append_audit(db, case.id, AuditKind.SCORED, {"features": features})

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
        attempt = _execute(db, case, decision, gated.action)
        result.executed = True
        result.attempt_id = attempt.id

    db.commit()
    return result


def execute_latest_decision(db: Session, case: Case) -> ActionAttempt:
    decision = db.scalar(
        select(Decision).where(Decision.case_id == case.id).order_by(Decision.created_at.desc())
    )
    if not decision:
        raise ValueError("no_decision")
    action = Action(decision.action)
    attempt = _execute(db, case, decision, action)
    db.commit()
    return attempt


def _execute(db: Session, case: Case, decision: Decision, action: Action) -> ActionAttempt:
    idem = f"{case.id}:{action.value}:{decision.id}"
    existing = db.scalar(select(ActionAttempt).where(ActionAttempt.idempotency_key == idem))
    if existing:
        return existing

    exec_result = execute_action(action, case.id, case.case_key, case.amount_paise)
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

    if action == Action.STOP:
        case.status = CaseStatus.STOPPED.value
    elif action == Action.ESCALATE:
        case.status = CaseStatus.ESCALATED.value
    else:
        case.status = CaseStatus.ACTING.value

    return attempt

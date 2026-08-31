"""Batch evaluation: Baseline A vs Rebound → lift_value (paired RNG)."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from rebound.db.models import Case, EvalCaseResult, EvalRun
from rebound.features import extract_features
from rebound.propose import propose_ev
from rebound.schemas.enums import Action, OutcomeResult
from rebound.scoring import action_cost, score_actions


@dataclass
class PolicyRunStats:
    policy_name: str
    cases: int
    recovered: int
    recovered_value: int
    intervention_cost: int
    stops: int
    escalations: int
    simulated_recoveries: int

    @property
    def net_value(self) -> int:
        return self.recovered_value - self.intervention_cost

    @property
    def recovery_rate(self) -> float:
        return self.recovered / self.cases if self.cases else 0.0


def baseline_a_action(case: Case) -> str:
    """Fixed ladder — no EV."""
    if case.attempt_n <= 2:
        return Action.SILENT_RETRY.value
    if case.attempt_n == 3:
        return Action.PAYMENT_LINK.value
    return Action.STOP.value


def baseline_b_action(case: Case) -> str:
    if case.attempt_n >= 4:
        return Action.STOP.value
    if case.failure_class in {"expired_card", "insufficient_funds"}:
        return Action.NOTIFY_UPDATE_METHOD.value
    return Action.PAYMENT_LINK.value


def _p_for_action(case: Case, action: str) -> float:
    if action in {Action.STOP.value, Action.ESCALATE.value}:
        return 0.0
    feats = extract_features(case)
    scores = score_actions(feats, case.amount_paise)
    return float(scores.get(action, {}).get("p_recover", 0.1))


def _run_policy_on_cases(
    db: Session,
    eval_run_id: str,
    cases: list[Case],
    policy_name: str,
    uniforms: np.ndarray,
) -> PolicyRunStats:
    """Paired comparison: same uniforms[i] reused across policies for case i."""
    recovered = 0
    recovered_value = 0
    cost = 0
    stops = 0
    escalations = 0
    simulated = 0

    for i, case in enumerate(cases):
        if policy_name == "baseline_a":
            action = baseline_a_action(case)
        elif policy_name == "baseline_b":
            action = baseline_b_action(case)
        else:
            payload = propose_ev(db, case, ignore_history=True)
            action = payload.action.value

        c = action_cost(action, case.amount_paise)
        cost += c
        p = _p_for_action(case, action)
        did_recover = bool(uniforms[i] < p) if p > 0 else False

        if action == Action.STOP.value:
            stops += 1
            outcome = OutcomeResult.STOPPED.value
            val = 0
            did_recover = False
        elif action == Action.ESCALATE.value:
            escalations += 1
            outcome = OutcomeResult.PENDING.value
            val = 0
            did_recover = False
        elif did_recover:
            recovered += 1
            recovered_value += case.amount_paise
            simulated += 1
            outcome = OutcomeResult.RECOVERED.value
            val = case.amount_paise
        else:
            outcome = OutcomeResult.FAILED.value
            val = 0

        db.add(
            EvalCaseResult(
                eval_run_id=eval_run_id,
                case_id=case.id,
                policy_name=policy_name,
                action=action,
                outcome=outcome,
                recovered_value_paise=val,
                cost_paise=c,
                detail_json=json.dumps({"simulated": did_recover, "p_recover": p}),
            )
        )

    return PolicyRunStats(
        policy_name=policy_name,
        cases=len(cases),
        recovered=recovered,
        recovered_value=recovered_value,
        intervention_cost=cost,
        stops=stops,
        escalations=escalations,
        simulated_recoveries=simulated,
    )


def run_eval(
    db: Session,
    *,
    batch_id: str | None = None,
    seed: int = 42,
    include_baseline_b: bool = True,
) -> dict[str, Any]:
    cases = list(db.scalars(select(Case).order_by(Case.created_at.asc())).all())
    if not cases:
        raise ValueError("no_cases")

    batch_id = batch_id or f"batch-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    run = EvalRun(id=str(uuid.uuid4()), batch_id=batch_id, aggregates_json="{}")
    db.add(run)
    db.flush()

    # One uniform per case — shared across policies (common random numbers)
    uniforms = np.random.default_rng(seed).random(len(cases))

    rebound = _run_policy_on_cases(db, run.id, cases, "rebound", uniforms)
    baseline = _run_policy_on_cases(db, run.id, cases, "baseline_a", uniforms)
    stats: dict[str, PolicyRunStats] = {"rebound": rebound, "baseline_a": baseline}
    if include_baseline_b:
        stats["baseline_b"] = _run_policy_on_cases(db, run.id, cases, "baseline_b", uniforms)

    def pack(s: PolicyRunStats) -> dict[str, Any]:
        return {
            "policy_name": s.policy_name,
            "cases": s.cases,
            "recovered": s.recovered,
            "recovery_rate": s.recovery_rate,
            "recovered_value": s.recovered_value,
            "intervention_cost": s.intervention_cost,
            "net_value": s.net_value,
            "stop_rate": s.stops / s.cases if s.cases else 0.0,
            "escalation_rate": s.escalations / s.cases if s.cases else 0.0,
            "simulated_share": s.simulated_recoveries / s.recovered if s.recovered else 0.0,
        }

    lift_value = rebound.net_value - baseline.net_value
    aggregates = {
        "batch_id": batch_id,
        "seed": seed,
        "lift_value": lift_value,
        "lift_value_label": "simulated_net_value_delta",
        "policies": {k: pack(v) for k, v in stats.items()},
        "honest_note": "Recoveries are simulated from scored probabilities; not real rupees.",
    }
    run.aggregates_json = json.dumps(aggregates)
    db.commit()
    return {"eval_run_id": run.id, **aggregates}

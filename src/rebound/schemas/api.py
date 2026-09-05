from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from rebound.schemas.enums import Action, CaseStatus, GateResult


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "rebound-api"
    version: str = "0.1.0"


class ProposalPayload(BaseModel):
    action: Action
    confidence: float = Field(ge=0.0, le=1.0)
    p_recover: float = Field(ge=0.0, le=1.0)
    ev: float = 0.0
    rationale: str = ""


class CaseOut(BaseModel):
    id: str
    case_key: str
    source: str
    status: CaseStatus
    amount_paise: int
    currency: str
    customer_ref: str
    failure_class: str
    attempt_n: int
    tenure_days: int
    method: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CaseDetailOut(CaseOut):
    failure_code: str | None = None
    external_event_id: str | None = None
    latest_decision_action: str | None = None
    latest_gate_result: GateResult | None = None


class AuditEventOut(BaseModel):
    id: str
    case_id: str
    kind: str
    payload: dict[str, Any]
    created_at: datetime

    model_config = {"from_attributes": True}


class MetricsSummary(BaseModel):
    cases_total: int = 0
    cases_open: int = 0
    cases_recovered: int = 0
    cases_stopped: int = 0
    cases_escalated: int = 0
    eval_runs: int = 0


class SyntheticIngestResponse(BaseModel):
    inserted: int
    skipped: int
    case_ids: list[str]


class StubMessage(BaseModel):
    detail: str
    next: str | None = None


class DecideResponse(BaseModel):
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


class ExecuteResponse(BaseModel):
    attempt_id: str
    case_id: str
    action: str
    mode: str
    response: dict[str, Any]
    razorpay_payment_link_id: str | None = None


class WebhookIngestResponse(BaseModel):
    case_id: str
    case_key: str
    created: bool
    reconciled: bool = False
    event_type: str = "unknown"

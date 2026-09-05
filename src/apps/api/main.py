from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound import __version__
from rebound.audit import append_audit
from rebound.config import get_settings
from rebound.db import Case, EvalRun, get_db, init_db
from rebound.db.models import ActionAttempt, AuditEvent, Decision
from rebound.ingest import (
    IngestValidationError,
    process_razorpay_webhook,
    reconcile_payment_link_state,
    verify_razorpay_webhook_signature,
)
from rebound.razorpay import (
    RazorpayMvpConfigurationError,
    RazorpayMvpRequestError,
    fetch_payment_link,
    fetch_subscription,
    fetch_subscription_invoices,
)
from rebound.schemas.api import (
    AuditEventOut,
    CaseDetailOut,
    CaseOut,
    DecideResponse,
    ExecuteResponse,
    HealthResponse,
    MetricsSummary,
    SyntheticIngestResponse,
    WebhookIngestResponse,
)
from rebound.schemas.enums import AuditKind, CaseSource, CaseStatus, GateResult
from rebound.execute import PaymentLinkExecutionError
from rebound.workflow import decide_case, execute_latest_decision

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Rebound API", version=__version__, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(version=__version__)


@app.get("/api/v1/metrics/summary", response_model=MetricsSummary)
def metrics_summary(db: Session = Depends(get_db)) -> MetricsSummary:
    def count_status(status: str) -> int:
        return db.scalar(select(func.count()).select_from(Case).where(Case.status == status)) or 0

    return MetricsSummary(
        cases_total=db.scalar(select(func.count()).select_from(Case)) or 0,
        cases_open=count_status(CaseStatus.OPEN.value),
        cases_recovered=count_status(CaseStatus.RECOVERED.value),
        cases_stopped=count_status(CaseStatus.STOPPED.value),
        cases_escalated=count_status(CaseStatus.ESCALATED.value),
        eval_runs=db.scalar(select(func.count()).select_from(EvalRun)) or 0,
    )


@app.get("/api/v1/cases", response_model=list[CaseOut])
def list_cases(db: Session = Depends(get_db), limit: int = 100) -> list[Case]:
    return list(db.scalars(select(Case).order_by(Case.created_at.desc()).limit(limit)).all())


@app.get("/api/v1/cases/{case_id}", response_model=CaseDetailOut)
def get_case(case_id: str, db: Session = Depends(get_db)) -> CaseDetailOut:
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    latest = db.scalar(
        select(Decision).where(Decision.case_id == case_id).order_by(Decision.created_at.desc())
    )
    gate = None
    if latest:
        try:
            gate = GateResult(latest.gate_result)
        except ValueError:
            gate = None
    return CaseDetailOut(
        id=case.id,
        case_key=case.case_key,
        source=case.source,
        status=CaseStatus(case.status),
        amount_paise=case.amount_paise,
        currency=case.currency,
        customer_ref=case.customer_ref,
        failure_class=case.failure_class,
        attempt_n=case.attempt_n,
        tenure_days=case.tenure_days,
        method=case.method,
        created_at=case.created_at,
        updated_at=case.updated_at,
        failure_code=case.failure_code,
        external_event_id=case.external_event_id,
        latest_decision_action=latest.action if latest else None,
        latest_gate_result=gate,
    )


@app.get("/api/v1/cases/{case_id}/audit", response_model=list[AuditEventOut])
def case_audit(case_id: str, db: Session = Depends(get_db)) -> list[AuditEventOut]:
    if not db.get(Case, case_id):
        raise HTTPException(status_code=404, detail="case not found")
    rows = db.scalars(
        select(AuditEvent).where(AuditEvent.case_id == case_id).order_by(AuditEvent.created_at.asc())
    ).all()
    return [
        AuditEventOut(
            id=r.id,
            case_id=r.case_id,
            kind=r.kind,
            payload=json.loads(r.payload_json or "{}"),
            created_at=r.created_at,
        )
        for r in rows
    ]


@app.post("/api/v1/ingest/synthetic", response_model=SyntheticIngestResponse)
def ingest_synthetic(db: Session = Depends(get_db)) -> SyntheticIngestResponse:
    sample_path = Path(__file__).resolve().parents[2] / "scripts" / "sample_batch.json"
    if not sample_path.exists():
        raise HTTPException(status_code=500, detail="sample_batch.json missing")
    rows = json.loads(sample_path.read_text(encoding="utf-8"))
    inserted = 0
    skipped = 0
    ids: list[str] = []
    for row in rows:
        existing = db.scalar(select(Case).where(Case.case_key == row["case_key"]))
        if existing:
            skipped += 1
            continue
        case = Case(
            case_key=row["case_key"],
            source=CaseSource.SYNTHETIC.value,
            status=CaseStatus.OPEN.value,
            amount_paise=row["amount_paise"],
            currency=row.get("currency", "INR"),
            customer_ref=row["customer_ref"],
            failure_code=row.get("failure_code"),
            failure_class=row.get("failure_class", "unknown"),
            attempt_n=row.get("attempt_n", 1),
            tenure_days=row.get("tenure_days", 30),
            method=row.get("method", "upi"),
            payload_json=json.dumps(row),
        )
        db.add(case)
        db.flush()
        append_audit(db, case.id, AuditKind.INGESTED, {"source": "synthetic", "case_key": case.case_key})
        ids.append(case.id)
        inserted += 1
    db.commit()
    return SyntheticIngestResponse(inserted=inserted, skipped=skipped, case_ids=ids)


@app.post("/api/v1/ingest/webhooks/razorpay", response_model=WebhookIngestResponse)
async def ingest_webhook(
    request: Request,
    payload: dict[str, Any],
    db: Session = Depends(get_db),
) -> WebhookIngestResponse:
    raw_body = await request.body()
    if settings.rebound_execution_mode == "mvp_mode" and not settings.razorpay_webhook_secret:
        raise HTTPException(status_code=503, detail="razorpay_mvp_webhook_secret_required")
    if not verify_razorpay_webhook_signature(
        raw_body,
        request.headers.get("X-Razorpay-Signature"),
        settings.razorpay_webhook_secret,
    ):
        raise HTTPException(status_code=401, detail="invalid_webhook_signature")
    try:
        result = process_razorpay_webhook(
            db,
            payload,
            event_id=request.headers.get("X-Razorpay-Event-Id"),
        )
    except IngestValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.commit()
    return WebhookIngestResponse(
        case_id=result.case.id,
        case_key=result.case.case_key,
        created=result.created,
        reconciled=result.reconciled,
        event_type=result.event_type,
    )


@app.post("/api/v1/cases/batch/decide")
def batch_decide(auto_execute: bool = True, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Decide (+ optional execute) all open cases — iteration helper.

    Registered before ``/cases/{case_id}/decide`` so ``batch`` is not parsed as an id.
    """
    open_cases = list(
        db.scalars(select(Case).where(Case.status == CaseStatus.OPEN.value)).all()
    )
    results = []
    for case in open_cases:
        r = decide_case(db, case, auto_execute=auto_execute)
        results.append(
            {
                "case_id": r.case_id,
                "gated_action": r.gated_action,
                "gate_result": r.gate_result,
                "executed": r.executed,
            }
        )
    return {"count": len(results), "results": results}


@app.post("/api/v1/cases/{case_id}/decide", response_model=DecideResponse)
def decide(case_id: str, auto_execute: bool = False, db: Session = Depends(get_db)) -> DecideResponse:
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    result = decide_case(db, case, auto_execute=auto_execute)
    return DecideResponse(
        case_id=result.case_id,
        proposal_id=result.proposal_id,
        decision_id=result.decision_id,
        proposed_action=result.proposed_action,
        gated_action=result.gated_action,
        gate_result=result.gate_result,
        gate_reason=result.gate_reason,
        rationale=result.rationale,
        confidence=result.confidence,
        ev=result.ev,
        executed=result.executed,
        attempt_id=result.attempt_id,
    )


@app.post("/api/v1/cases/{case_id}/execute", response_model=ExecuteResponse)
def execute(case_id: str, db: Session = Depends(get_db)) -> ExecuteResponse:
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    try:
        attempt = execute_latest_decision(db, case)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PaymentLinkExecutionError as exc:
        # Do not create an attempt/outcome when the external MVP-mode request failed.
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ExecuteResponse(
        attempt_id=attempt.id,
        case_id=case.id,
        action=attempt.action,
        mode=attempt.mode,
        response=json.loads(attempt.response_json or "{}"),
        razorpay_payment_link_id=attempt.razorpay_payment_link_id,
    )


@app.post("/api/v1/cases/{case_id}/refresh-payment-link")
def refresh_payment_link(case_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Read a Rebound-created Test Mode link and reconcile a terminal state."""
    case = db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    attempt = db.scalar(
        select(ActionAttempt)
        .where(
            ActionAttempt.case_id == case_id,
            ActionAttempt.mode == "mvp_mode",
            ActionAttempt.razorpay_payment_link_id.is_not(None),
        )
        .order_by(ActionAttempt.created_at.desc())
    )
    if not attempt or not attempt.razorpay_payment_link_id:
        raise HTTPException(status_code=400, detail="no_mvp_payment_link")
    try:
        link = fetch_payment_link(attempt.razorpay_payment_link_id)
        reconciled_case = reconcile_payment_link_state(
            db,
            link,
            source="razorpay_api_read",
        )
    except RazorpayMvpConfigurationError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RazorpayMvpRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    db.commit()
    return {
        "case_id": case.id,
        "payment_link_id": attempt.razorpay_payment_link_id,
        "payment_link_status": link.get("status"),
        "reconciled": reconciled_case is not None,
        "case_status": reconciled_case.status if reconciled_case else case.status,
    }


@app.get("/api/v1/razorpay/subscriptions/{subscription_id}")
def get_razorpay_subscription(subscription_id: str) -> dict[str, Any]:
    """Read one Razorpay Test Mode subscription; no changes are permitted."""
    try:
        return fetch_subscription(subscription_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RazorpayMvpRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/v1/razorpay/subscriptions/{subscription_id}/invoices")
def get_razorpay_subscription_invoices(subscription_id: str) -> dict[str, Any]:
    """Read Razorpay Test Mode invoices for a subscription; no changes are permitted."""
    try:
        return fetch_subscription_invoices(subscription_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RazorpayMvpRequestError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/v1/eval/runs")
def list_eval_runs(db: Session = Depends(get_db), limit: int = 20) -> list[dict[str, Any]]:
    rows = list(db.scalars(select(EvalRun).order_by(EvalRun.created_at.desc()).limit(limit)).all())
    out = []
    for run in rows:
        agg = json.loads(run.aggregates_json or "{}")
        out.append(
            {
                "eval_run_id": run.id,
                "batch_id": run.batch_id,
                "lift_value": agg.get("lift_value"),
                "created_at": run.created_at.isoformat() if run.created_at else None,
            }
        )
    return out


@app.post("/api/v1/eval/runs")
def create_eval_run(
    seed: int = 42,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    from rebound.eval import run_eval

    try:
        return run_eval(db, seed=seed)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/v1/eval/runs/{run_id}")
def get_eval_run(run_id: str, db: Session = Depends(get_db)) -> dict[str, Any]:
    run = db.get(EvalRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="eval run not found")
    return {"eval_run_id": run.id, "batch_id": run.batch_id, **json.loads(run.aggregates_json or "{}")}


@app.get("/api/v1/audit/recent")
def recent_audit(db: Session = Depends(get_db), limit: int = 50) -> list[AuditEventOut]:
    rows = list(
        db.scalars(select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit)).all()
    )
    return [
        AuditEventOut(
            id=r.id,
            case_id=r.case_id,
            kind=r.kind,
            payload=json.loads(r.payload_json or "{}"),
            created_at=r.created_at,
        )
        for r in rows
    ]

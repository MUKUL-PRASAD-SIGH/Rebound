from __future__ import annotations

import json
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from rebound import __version__
from rebound.audit import append_audit
from rebound.config import get_settings
from rebound.db import Case, EvalRun, get_db, init_db
from rebound.db.models import AuditEvent, Decision
from rebound.schemas import (
    AuditEventOut,
    CaseDetailOut,
    CaseOut,
    HealthResponse,
    MetricsSummary,
    StubMessage,
    SyntheticIngestResponse,
)
from rebound.schemas.enums import AuditKind, CaseSource, CaseStatus

settings = get_settings()

app = FastAPI(title="Rebound API", version=__version__)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


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
        from rebound.schemas.enums import GateResult

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
    """Seed a small demo batch if empty / always append unique keys."""
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


@app.post("/api/v1/ingest/webhooks/razorpay", response_model=StubMessage)
def ingest_webhook_stub() -> StubMessage:
    return StubMessage(
        detail="Webhook ingest scaffolded — signature verify + case upsert on Day 04",
        next="POST payload shape accepted later; use /ingest/synthetic for now",
    )


@app.post("/api/v1/cases/{case_id}/decide", response_model=StubMessage)
def decide_stub(case_id: str, db: Session = Depends(get_db)) -> StubMessage:
    if not db.get(Case, case_id):
        raise HTTPException(status_code=404, detail="case not found")
    return StubMessage(detail="decide pipeline scaffolded — wire propose→gate→execute on Day 04/05")


@app.post("/api/v1/cases/{case_id}/execute", response_model=StubMessage)
def execute_stub(case_id: str, db: Session = Depends(get_db)) -> StubMessage:
    if not db.get(Case, case_id):
        raise HTTPException(status_code=404, detail="case not found")
    return StubMessage(detail="execute scaffolded — Payment Link / dry_run on Day 04")


@app.post("/api/v1/eval/runs", response_model=StubMessage)
def eval_stub() -> StubMessage:
    return StubMessage(detail="eval runner scaffolded — Baseline A vs Rebound lift on Day 05/06")


@app.get("/api/v1/eval/runs/{run_id}", response_model=StubMessage)
def eval_get_stub(run_id: str) -> StubMessage:
    return StubMessage(detail=f"eval run {run_id} not implemented yet")

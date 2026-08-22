from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _uuid() -> str:
    return str(uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    source: Mapped[str] = mapped_column(String(32))
    external_event_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="open", index=True)
    amount_paise: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(8), default="INR")
    customer_ref: Mapped[str] = mapped_column(String(128))
    failure_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    failure_class: Mapped[str] = mapped_column(String(64), default="unknown")
    attempt_n: Mapped[int] = mapped_column(Integer, default=1)
    tenure_days: Mapped[int] = mapped_column(Integer, default=30)
    method: Mapped[str] = mapped_column(String(32), default="upi")
    payload_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    proposals: Mapped[list[Proposal]] = relationship(back_populates="case")
    decisions: Mapped[list[Decision]] = relationship(back_populates="case")
    action_attempts: Mapped[list[ActionAttempt]] = relationship(back_populates="case")
    outcomes: Mapped[list[Outcome]] = relationship(back_populates="case")
    audit_events: Mapped[list[AuditEvent]] = relationship(back_populates="case")


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    action: Mapped[str] = mapped_column(String(64))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    ev: Mapped[float] = mapped_column(Float, default=0.0)
    p_recover: Mapped[float] = mapped_column(Float, default=0.0)
    rationale: Mapped[str] = mapped_column(Text, default="")
    proposer: Mapped[str] = mapped_column(String(32), default="rules")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    case: Mapped[Case] = relationship(back_populates="proposals")


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    proposal_id: Mapped[str | None] = mapped_column(ForeignKey("proposals.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(64))
    gate_result: Mapped[str] = mapped_column(String(32))
    gate_reason: Mapped[str] = mapped_column(Text, default="")
    policy_version: Mapped[str] = mapped_column(String(32), default="mvp-v1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    case: Mapped[Case] = relationship(back_populates="decisions")


class ActionAttempt(Base):
    __tablename__ = "action_attempts"
    __table_args__ = (UniqueConstraint("idempotency_key", name="uq_action_idempotency"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"))
    action: Mapped[str] = mapped_column(String(64))
    mode: Mapped[str] = mapped_column(String(32))
    request_json: Mapped[str] = mapped_column(Text, default="{}")
    response_json: Mapped[str] = mapped_column(Text, default="{}")
    razorpay_payment_link_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    case: Mapped[Case] = relationship(back_populates="action_attempts")


class Outcome(Base):
    __tablename__ = "outcomes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    action_attempt_id: Mapped[str | None] = mapped_column(
        ForeignKey("action_attempts.id"), nullable=True
    )
    result: Mapped[str] = mapped_column(String(32))
    value_paise: Mapped[int] = mapped_column(Integer, default=0)
    label: Mapped[str] = mapped_column(String(32))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    case: Mapped[Case] = relationship(back_populates="outcomes")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    payload_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    case: Mapped[Case] = relationship(back_populates="audit_events")


class EvalRun(Base):
    __tablename__ = "eval_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    batch_id: Mapped[str] = mapped_column(String(64), index=True)
    aggregates_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    results: Mapped[list[EvalCaseResult]] = relationship(back_populates="eval_run")


class EvalCaseResult(Base):
    __tablename__ = "eval_case_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    eval_run_id: Mapped[str] = mapped_column(ForeignKey("eval_runs.id"), index=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("cases.id"), index=True)
    policy_name: Mapped[str] = mapped_column(String(32))  # baseline_a | rebound
    action: Mapped[str] = mapped_column(String(64))
    outcome: Mapped[str] = mapped_column(String(32))
    recovered_value_paise: Mapped[int] = mapped_column(Integer, default=0)
    cost_paise: Mapped[int] = mapped_column(Integer, default=0)
    detail_json: Mapped[str] = mapped_column(Text, default="{}")

    eval_run: Mapped[EvalRun] = relationship(back_populates="results")

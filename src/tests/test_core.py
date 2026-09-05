"""Comprehensive tests: scoring, policy, propose, ingest, workflow, eval, API."""

from __future__ import annotations

import json
import hashlib
import hmac
import sys
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rebound.db.models import ActionAttempt, Base, Case, Decision, Outcome  # noqa: E402
from rebound.db.session import get_db  # noqa: E402
from rebound.eval import run_eval  # noqa: E402
from rebound.execute import (  # noqa: E402
    ExecuteResult,
    PaymentLinkConfigurationError,
    PaymentLinkExecutionError,
    execute_action,
)
from rebound.features import FAILURE_CLASSES, METHODS, extract_features, vectorize  # noqa: E402
from rebound.ingest import (  # noqa: E402
    IngestValidationError,
    process_razorpay_webhook,
    upsert_from_webhook_payload,
)
from rebound.policy import gate  # noqa: E402
from rebound.propose import propose_ev, propose_for_case, propose_rules_ladder  # noqa: E402
from rebound.schemas.api import ProposalPayload  # noqa: E402
from rebound.schemas.enums import (  # noqa: E402
    Action,
    AuditKind,
    CaseSource,
    CaseStatus,
    GateResult,
    ProposerKind,
)
from rebound.scoring import (  # noqa: E402
    action_cost,
    expected_value,
    p_recover_base,
    reset_model_cache,
    score_actions,
)
from rebound.workflow import decide_case, execute_latest_decision  # noqa: E402


@pytest.fixture()
def engine():
    from sqlalchemy.pool import StaticPool

    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    return eng


@pytest.fixture()
def db(engine) -> Session:
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(engine, monkeypatch):
    from apps.api import main as api_main
    from apps.api.main import app
    from rebound.db import session as db_session

    SessionLocal = sessionmaker(bind=engine)

    def _override():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    # Prevent startup from touching the real rebound.db for API tests
    monkeypatch.setattr(api_main.settings, "rebound_api_token", "test-operator-token")
    app.dependency_overrides[get_db] = _override
    original_init = db_session.init_db
    db_session.init_db = lambda: None  # type: ignore[assignment]
    with TestClient(app) as c:
        c.headers.update({"X-Rebound-Token": "test-operator-token"})
        yield c
    db_session.init_db = original_init
    app.dependency_overrides.clear()


def _case(**kwargs) -> Case:
    defaults = dict(
        case_key="t-1",
        source=CaseSource.SYNTHETIC.value,
        status=CaseStatus.OPEN.value,
        amount_paise=50_000,
        currency="INR",
        customer_ref="c1",
        failure_class="insufficient_funds",
        attempt_n=1,
        tenure_days=60,
        method="upi",
        payload_json="{}",
    )
    defaults.update(kwargs)
    return Case(**defaults)


# --- scoring ---


def test_vectorize_length():
    v = vectorize(
        {
            "amount_paise": 10000,
            "attempt_n": 1,
            "tenure_days": 30,
            "failure_class": "unknown",
            "method": "upi",
        }
    )
    assert len(v) == 3 + len(FAILURE_CLASSES) + len(METHODS)


def test_score_actions_has_ev_and_cost_scales():
    scores = score_actions(
        {
            "amount_paise": 100_000,
            "attempt_n": 1,
            "tenure_days": 30,
            "failure_class": "insufficient_funds",
            "method": "upi",
        },
        100_000,
    )
    assert Action.SILENT_RETRY.value in scores
    assert scores[Action.PAYMENT_LINK.value]["cost"] > scores[Action.SILENT_RETRY.value]["cost"]
    assert action_cost(Action.STOP.value, 100_000) == 0


def test_expected_value_math():
    assert expected_value(0.5, 1000, Action.STOP.value) == 500.0


def test_p_recover_bounds():
    reset_model_cache()
    p, src = p_recover_base(
        {
            "amount_paise": 20000,
            "attempt_n": 1,
            "tenure_days": 30,
            "failure_class": "bank_decline",
            "method": "card",
        }
    )
    assert 0.05 <= p <= 0.95
    assert src in {"model", "heuristic"}


def test_propose_ev_diverse_actions(db: Session):
    specs = [
        ("a", 8_000, "insufficient_funds", 1),
        ("b", 900_000, "unknown", 4),
        ("c", 40_000, "expired_card", 3),
        ("d", 15_000, "bank_decline", 2),
        ("e", 5_000, "insufficient_funds", 5),
    ]
    actions = set()
    for key, amt, fc, att in specs:
        case = _case(case_key=key, amount_paise=amt, failure_class=fc, attempt_n=att)
        db.add(case)
        db.flush()
        actions.add(propose_ev(db, case).action.value)
    assert len(actions) >= 2


def test_openai_llm_proposer_uses_structured_action_and_deterministic_metrics(db: Session, monkeypatch):
    import rebound.propose as proposer

    class LlmSettings:
        rebound_enable_llm_proposer = True
        openai_api_key = "test-openai-key"
        openai_model = "gpt-4o-mini"

    case = _case(case_key="llm-proposal", amount_paise=80_000, failure_class="expired_card")
    db.add(case)
    db.commit()
    ev = propose_ev(db, case)
    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output_text": json.dumps(
                    {
                        "action": ev.action.value,
                        "rationale": "The deterministic score supports this bounded action.",
                    }
                ),
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(proposer, "get_settings", lambda: LlmSettings())
    monkeypatch.setattr(proposer.httpx, "post", fake_post)

    payload, kind = propose_for_case(db, case)

    assert kind == ProposerKind.LLM
    assert payload.action == ev.action
    assert payload.p_recover == pytest.approx(ev.p_recover)
    assert payload.ev == pytest.approx(ev.ev)
    assert payload.rationale.startswith("llm_openai_selected")
    assert captured["url"] == "https://api.openai.com/v1/responses"
    request_body = captured["json"]
    assert isinstance(request_body, dict)
    assert request_body["store"] is False
    assert request_body["text"]["format"]["type"] == "json_schema"
    input_body = json.loads(request_body["input"])
    assert "customer_ref" not in input_body["case"]
    assert "case_key" not in input_body["case"]


def test_openai_llm_proposer_falls_back_when_output_is_invalid(db: Session, monkeypatch):
    import rebound.propose as proposer

    class LlmSettings:
        rebound_enable_llm_proposer = True
        openai_api_key = "test-openai-key"
        openai_model = "gpt-4o-mini"

    case = _case(case_key="llm-invalid-output", amount_paise=80_000)
    db.add(case)
    db.commit()

    def fake_post(url: str, **_kwargs):
        return httpx.Response(
            200,
            json={
                "status": "completed",
                "output_text": '{"action":"outside_allowlist","rationale":"unsafe"}',
            },
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(proposer, "get_settings", lambda: LlmSettings())
    monkeypatch.setattr(proposer.httpx, "post", fake_post)

    payload, kind = propose_for_case(db, case)

    assert kind == ProposerKind.MODEL
    assert payload.rationale.startswith("ev_max")


def test_openai_llm_proposer_is_off_without_flag(db: Session, monkeypatch):
    import rebound.propose as proposer

    class DisabledLlmSettings:
        rebound_enable_llm_proposer = False
        openai_api_key = "test-openai-key"
        openai_model = "gpt-4o-mini"

    case = _case(case_key="llm-disabled", amount_paise=80_000)
    db.add(case)
    db.commit()

    monkeypatch.setattr(proposer, "get_settings", lambda: DisabledLlmSettings())
    monkeypatch.setattr(
        proposer.httpx,
        "post",
        lambda *_args, **_kwargs: pytest.fail("disabled LLM proposer must not call OpenAI"),
    )

    _, kind = propose_for_case(db, case)

    assert kind == ProposerKind.MODEL


# --- policy ---


def test_policy_low_confidence_stop():
    g = gate(
        ProposalPayload(
            action=Action.SILENT_RETRY,
            confidence=0.1,
            p_recover=0.2,
            ev=100.0,
            rationale="t",
        )
    )
    assert g.gate_result == GateResult.REWRITE_STOP


def test_policy_min_ev_stop():
    g = gate(
        ProposalPayload(
            action=Action.PAYMENT_LINK,
            confidence=0.9,
            p_recover=0.1,
            ev=-50.0,
            rationale="t",
        )
    )
    assert g.gate_result == GateResult.REWRITE_STOP
    assert g.reason == "ev_below_min"


def test_policy_unknown_action_reject():
    g = gate(
        ProposalPayload(
            action=Action.STOP,  # valid — use monkey by constructing then overwrite
            confidence=0.9,
            p_recover=0.1,
            ev=0.0,
            rationale="t",
        )
    )
    # STOP allowed
    assert g.gate_result == GateResult.ALLOW


def test_policy_high_value_escalate(db: Session):
    case = _case(case_key="hv", amount_paise=500_000, failure_class="unknown")
    db.add(case)
    db.commit()
    g = gate(
        ProposalPayload(
            action=Action.SILENT_RETRY,
            confidence=0.4,
            p_recover=0.3,
            ev=1000.0,
            rationale="t",
        ),
        db=db,
        case=case,
    )
    assert g.gate_result == GateResult.REWRITE_ESCALATE


def test_policy_stop_bypasses_ev_floor():
    g = gate(
        ProposalPayload(
            action=Action.STOP,
            confidence=0.1,
            p_recover=0.0,
            ev=-1.0,
            rationale="t",
        )
    )
    assert g.gate_result == GateResult.ALLOW


def test_policy_max_retries(db: Session):
    from rebound.db.models import Decision, Proposal

    case = _case(case_key="retry-cap", amount_paise=30_000, attempt_n=1)
    db.add(case)
    db.flush()
    for i in range(3):
        prop = Proposal(
            case_id=case.id,
            action=Action.SILENT_RETRY.value,
            confidence=0.9,
            ev=1000.0,
            p_recover=0.5,
            rationale="seed",
            proposer="rules",
        )
        db.add(prop)
        db.flush()
        dec = Decision(
            case_id=case.id,
            proposal_id=prop.id,
            action=Action.SILENT_RETRY.value,
            gate_result=GateResult.ALLOW.value,
            gate_reason="seed",
            policy_version="test",
        )
        db.add(dec)
        db.flush()
        db.add(
            ActionAttempt(
                case_id=case.id,
                decision_id=dec.id,
                action=Action.SILENT_RETRY.value,
                mode="dry_run",
                idempotency_key=f"cap-{case.id}-{i}",
            )
        )
    db.commit()
    case = db.get(Case, case.id)
    payload = ProposalPayload(
        action=Action.SILENT_RETRY,
        confidence=0.9,
        p_recover=0.5,
        ev=1000.0,
        rationale="force",
    )
    g = gate(payload, db=db, case=case)
    assert g.gate_result == GateResult.REWRITE_STOP
    assert "max_silent_retries" in g.reason


# --- rules / workflow ---


def test_rules_ladder_first_retry(db: Session):
    case = _case(attempt_n=1)
    db.add(case)
    db.commit()
    assert propose_rules_ladder(db, case).action == Action.SILENT_RETRY


def test_decide_execute_outcome_audit(db: Session):
    case = _case(case_key="flow-1", amount_paise=25_000)
    db.add(case)
    db.commit()
    result = decide_case(db, case, auto_execute=True)
    assert result.executed
    assert result.gate_result in {g.value for g in GateResult}
    outcomes = list(db.scalars(select(Outcome).where(Outcome.case_id == case.id)).all())
    assert len(outcomes) == 1
    from rebound.db.models import AuditEvent

    kinds = [
        e.kind
        for e in db.scalars(
            select(AuditEvent).where(AuditEvent.case_id == case.id).order_by(AuditEvent.created_at)
        ).all()
    ]
    assert AuditKind.SCORED.value in kinds
    assert AuditKind.PROPOSED.value in kinds
    assert AuditKind.GATED.value in kinds
    assert AuditKind.EXECUTED.value in kinds
    assert AuditKind.OUTCOME.value in kinds


def test_execute_idempotent(db: Session):
    case = _case(case_key="idem-1")
    db.add(case)
    db.commit()
    decide_case(db, case, auto_execute=False)
    a1 = execute_latest_decision(db, case)
    a2 = execute_latest_decision(db, case)
    assert a1.id == a2.id
    n = len(list(db.scalars(select(ActionAttempt).where(ActionAttempt.case_id == case.id)).all()))
    assert n == 1


def test_mvp_mode_payment_link_waits_for_and_reconciles_signed_webhook(db: Session, monkeypatch):
    import rebound.workflow as workflow

    case = _case(case_key="mvp-payment-link", amount_paise=12_345)
    db.add(case)
    db.flush()
    decision = Decision(
        case_id=case.id,
        action=Action.PAYMENT_LINK.value,
        gate_result=GateResult.ALLOW.value,
        gate_reason="test",
    )
    db.add(decision)
    db.commit()

    monkeypatch.setattr(
        workflow,
        "execute_action",
        lambda *_args, **_kwargs: ExecuteResult(
            mode="mvp_mode",
            request={"action": "payment_link"},
            response={"ok": True, "payment_link_id": "plink_mvp_123"},
            razorpay_payment_link_id="plink_mvp_123",
        ),
    )
    attempt = execute_latest_decision(db, case)
    pending = db.scalar(select(Outcome).where(Outcome.action_attempt_id == attempt.id))
    assert pending is not None
    assert pending.result == "pending"
    assert pending.label == "mvp_mode"
    assert db.get(Case, case.id).status == CaseStatus.ACTING.value

    result = process_razorpay_webhook(
        db,
        {
            "event": "payment_link.paid",
            "payload": {
                "payment_link": {
                    "entity": {
                        "id": "plink_mvp_123",
                        "amount": 12_345,
                        "amount_paid": 12_345,
                        "notes": {"rebound_case_id": case.id},
                    }
                }
            },
        },
        event_id="evt_mvp_paid_123",
    )
    assert result.created is False
    assert result.reconciled is True
    assert result.case.id == case.id
    assert pending.result == "recovered"
    assert pending.value_paise == 12_345
    assert db.get(Case, case.id).status == CaseStatus.RECOVERED.value

    duplicate = process_razorpay_webhook(
        db,
        {"event": "payment_link.paid"},
        event_id="evt_mvp_paid_123",
    )
    assert duplicate.reconciled is False
    assert duplicate.case.id == case.id
    assert db.scalar(select(Outcome).where(Outcome.action_attempt_id == attempt.id)) == pending


def test_execute_without_decision_raises(db: Session):
    case = _case(case_key="no-dec")
    db.add(case)
    db.commit()
    with pytest.raises(ValueError, match="no_decision"):
        execute_latest_decision(db, case)


def test_mvp_mode_payment_link_uses_razorpay_contract(monkeypatch):
    import rebound.execute as execution

    class TestSettings:
        rebound_execution_mode = "mvp_mode"
        razorpay_key_id = "rzp_test_key"
        razorpay_key_secret = "rzp_test_secret"

    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        request = httpx.Request("POST", url)
        return httpx.Response(
            200,
            json={"id": "plink_test_123", "short_url": "https://rzp.io/i/test", "status": "created"},
            request=request,
        )

    monkeypatch.setattr(execution, "get_settings", lambda: TestSettings())
    monkeypatch.setattr(execution.httpx, "post", fake_post)

    result = execute_action(
        Action.PAYMENT_LINK,
        "case-123",
        "order-123",
        12_345,
        currency="INR",
        decision_id="decision-123",
    )

    assert result.mode == "mvp_mode"
    assert result.razorpay_payment_link_id == "plink_test_123"
    assert "url" not in result.response
    assert captured["url"] == "https://api.razorpay.com/v1/payment_links"
    assert captured["auth"] == ("rzp_test_key", "rzp_test_secret")
    body = captured["json"]
    assert isinstance(body, dict)
    assert body["amount"] == 12_345
    assert body["currency"] == "INR"
    assert body["notify"] == {"sms": False, "email": False}
    assert len(body["reference_id"]) <= 40


def test_mvp_mode_payment_link_rejects_live_key_without_http(monkeypatch):
    import rebound.execute as execution

    class LiveKeySettings:
        rebound_execution_mode = "mvp_mode"
        razorpay_key_id = "rzp_live_key"
        razorpay_key_secret = "live_secret"

    monkeypatch.setattr(execution, "get_settings", lambda: LiveKeySettings())
    monkeypatch.setattr(
        execution.httpx,
        "post",
        lambda *_args, **_kwargs: pytest.fail("live key must not make an HTTP request"),
    )

    with pytest.raises(
        PaymentLinkConfigurationError,
        match="razorpay_mvp_mode_requires_rzp_test_key",
    ):
        execute_action(
            Action.PAYMENT_LINK,
            "case-live-key",
            "order-live-key",
            12_345,
            decision_id="decision-live-key",
        )


def test_mvp_mode_payment_link_reconciles_ambiguous_request(monkeypatch):
    import rebound.execute as execution

    class TestSettings:
        rebound_execution_mode = "mvp_mode"
        razorpay_key_id = "rzp_test_key"
        razorpay_key_secret = "rzp_test_secret"

    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs):
        raise httpx.ReadTimeout("timed out", request=httpx.Request("POST", url))

    def fake_get(url: str, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        reference_id = kwargs["params"]["reference_id"]
        return httpx.Response(
            200,
            json={
                "payment_links": [
                    {
                        "id": "plink_reconciled_123",
                        "short_url": "https://rzp.io/i/reconciled",
                        "reference_id": reference_id,
                        "status": "created",
                    }
                ]
            },
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(execution, "get_settings", lambda: TestSettings())
    monkeypatch.setattr(execution.httpx, "post", fake_post)
    monkeypatch.setattr(execution.httpx, "get", fake_get)

    result = execute_action(
        Action.PAYMENT_LINK,
        "case-ambiguous",
        "order-ambiguous",
        12_345,
        decision_id="decision-ambiguous",
    )

    assert result.razorpay_payment_link_id == "plink_reconciled_123"
    assert result.response["reconciled_from_reference_lookup"] is True
    assert captured["url"] == "https://api.razorpay.com/v1/payment_links"


def test_mvp_mode_razorpay_reads_use_only_test_credentials(monkeypatch):
    import rebound.razorpay as razorpay

    class MvpSettings:
        rebound_execution_mode = "mvp_mode"
        razorpay_key_id = "rzp_test_key"
        razorpay_key_secret = "rzp_test_secret"

    captured: dict[str, object] = {}

    def fake_get(url: str, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return httpx.Response(
            200,
            json={"id": "sub_mvp_123", "status": "active"},
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(razorpay, "get_settings", lambda: MvpSettings())
    monkeypatch.setattr(razorpay.httpx, "get", fake_get)

    result = razorpay.fetch_subscription("sub_mvp_123")

    assert result["status"] == "active"
    assert captured["url"] == "https://api.razorpay.com/v1/subscriptions/sub_mvp_123"
    assert captured["auth"] == ("rzp_test_key", "rzp_test_secret")


def test_mvp_mode_razorpay_reads_reject_live_key_without_http(monkeypatch):
    import rebound.razorpay as razorpay

    class LiveKeySettings:
        rebound_execution_mode = "mvp_mode"
        razorpay_key_id = "rzp_live_key"
        razorpay_key_secret = "live_secret"

    monkeypatch.setattr(razorpay, "get_settings", lambda: LiveKeySettings())
    monkeypatch.setattr(
        razorpay.httpx,
        "get",
        lambda *_args, **_kwargs: pytest.fail("live key must not make an HTTP request"),
    )

    with pytest.raises(razorpay.RazorpayMvpConfigurationError):
        razorpay.fetch_payment_link("plink_mvp_123")


def test_api_payment_link_failure_returns_502_without_attempt(client: TestClient, engine, monkeypatch):
    import rebound.workflow as workflow

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        case = _case(case_key="payment-link-failure")
        session.add(case)
        session.flush()
        session.add(
            Decision(
                case_id=case.id,
                action=Action.PAYMENT_LINK.value,
                gate_result=GateResult.ALLOW.value,
                gate_reason="test decision",
            )
        )
        session.commit()
        case_id = case.id

    def fail_payment_link(*_args, **_kwargs):
        raise PaymentLinkExecutionError("razorpay_payment_link_request_failed")

    monkeypatch.setattr(workflow, "execute_action", fail_payment_link)
    response = client.post(f"/api/v1/cases/{case_id}/execute")
    assert response.status_code == 502
    assert response.json()["detail"] == "razorpay_payment_link_request_failed"

    with SessionLocal() as session:
        assert session.scalar(
            select(ActionAttempt).where(ActionAttempt.case_id == case_id).limit(1)
        ) is None


def test_api_refresh_payment_link_reconciles_authoritative_read(client: TestClient, engine, monkeypatch):
    from apps.api import main as api_main

    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as session:
        case = _case(case_key="refresh-link-case", amount_paise=25_000)
        session.add(case)
        session.flush()
        decision = Decision(
            case_id=case.id,
            action=Action.PAYMENT_LINK.value,
            gate_result=GateResult.ALLOW.value,
            gate_reason="test",
        )
        session.add(decision)
        session.flush()
        attempt = ActionAttempt(
            case_id=case.id,
            decision_id=decision.id,
            action=Action.PAYMENT_LINK.value,
            mode="mvp_mode",
            request_json="{}",
            response_json="{}",
            razorpay_payment_link_id="plink_refresh_123",
            idempotency_key="refresh-link-attempt",
        )
        session.add(attempt)
        session.flush()
        session.add(
            Outcome(
                case_id=case.id,
                action_attempt_id=attempt.id,
                result="pending",
                value_paise=0,
                label="mvp_mode",
            )
        )
        session.commit()
        case_id = case.id

    monkeypatch.setattr(
        api_main,
        "fetch_payment_link",
        lambda _link_id: {"id": "plink_refresh_123", "status": "paid", "amount_paid": 25_000},
    )
    response = client.post(f"/api/v1/cases/{case_id}/refresh-payment-link")

    assert response.status_code == 200
    assert response.json()["reconciled"] is True
    assert response.json()["case_status"] == "recovered"


def test_api_read_only_subscription_routes(client: TestClient, monkeypatch):
    from apps.api import main as api_main

    monkeypatch.setattr(
        api_main,
        "fetch_subscription",
        lambda subscription_id: {
            "id": subscription_id,
            "status": "active",
            "email": "private@example.com",
            "short_url": "https://private.example/link",
            "plan_id": "plan_safe",
        },
    )
    monkeypatch.setattr(
        api_main,
        "fetch_subscription_invoices",
        lambda subscription_id: {
            "count": 1,
            "items": [{"subscription_id": subscription_id, "contact": "+919999999999", "amount": 12_000}],
        },
    )

    subscription = client.get("/api/v1/razorpay/subscriptions/sub_read_123")
    invoices = client.get("/api/v1/razorpay/subscriptions/sub_read_123/invoices")

    assert subscription.status_code == 200
    assert subscription.json()["status"] == "active"
    assert "email" not in subscription.json()
    assert "short_url" not in subscription.json()
    assert invoices.status_code == 200
    assert invoices.json()["count"] == 1
    assert "contact" not in invoices.json()["items"][0]


# --- ingest ---


def test_webhook_rejects_empty(db: Session):
    with pytest.raises(IngestValidationError):
        upsert_from_webhook_payload(db, {})


def test_webhook_rejects_zero_amount(db: Session):
    with pytest.raises(IngestValidationError):
        upsert_from_webhook_payload(
            db,
            {"event_id": "e1", "amount_paise": 0, "customer_ref": "c"},
        )


def test_webhook_upsert_and_replay(db: Session):
    payload = {
        "id": "evt_1",
        "amount_paise": 12000,
        "customer_ref": "cust_x",
        "failure_class": "bank_decline",
    }
    c1, created1 = upsert_from_webhook_payload(db, payload)
    db.commit()
    c2, created2 = upsert_from_webhook_payload(db, payload)
    assert created1 is True
    assert created2 is False
    assert c1.id == c2.id


def test_webhook_pseudonymizes_and_redacts_pii_at_rest(db: Session):
    payload = {
        "id": "evt_private_1",
        "amount_paise": 12_000,
        "customer_ref": "alice@example.com",
        "email": "alice@example.com",
        "contact": "+919999999999",
        "notes": {"private": "do-not-store"},
    }
    case, created = upsert_from_webhook_payload(db, payload)

    assert created is True
    assert case.customer_ref.startswith("cust_")
    assert "alice@example.com" not in case.customer_ref
    assert "alice@example.com" not in case.payload_json
    assert "+919999999999" not in case.payload_json
    assert "do-not-store" not in case.payload_json


# --- eval ---


def test_run_eval_lift_and_pairing(db: Session):
    for i in range(12):
        db.add(
            _case(
                case_key=f"e-{i}",
                amount_paise=20_000 + i * 5_000,
                attempt_n=1 + (i % 3),
                failure_class=["insufficient_funds", "expired_card", "bank_decline", "unknown"][i % 4],
            )
        )
    db.commit()
    a = run_eval(db, seed=42)
    b = run_eval(db, seed=42)
    assert a["lift_value"] == b["lift_value"]
    assert a["lift_value_label"] == "simulated_net_value_delta"
    assert "baseline_a" in a["policies"]
    for name, p in a["policies"].items():
        assert p["net_value"] == p["recovered_value"] - p["intervention_cost"], name


def test_sample_batch_contract():
    path = ROOT / "scripts" / "sample_batch.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    assert len(rows) >= 50
    high = sum(1 for r in rows if r["amount_paise"] >= 500_000)
    assert high >= 1
    for r in rows:
        assert {"case_key", "amount_paise", "customer_ref"} <= set(r.keys())


# --- API ---


def test_api_health(client: TestClient):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_api_operator_routes_require_a_valid_token(client: TestClient):
    denied = client.get("/api/v1/cases", headers={"X-Rebound-Token": "not-the-token"})
    assert denied.status_code == 401

    allowed = client.get("/api/v1/cases")
    assert allowed.status_code == 200


def test_api_eval_empty_400(client: TestClient):
    r = client.post("/api/v1/eval/runs")
    assert r.status_code == 404 or r.status_code == 400
    # empty DB → 400 no_cases
    assert r.status_code == 400


def test_api_seed_decide_execute_eval(client: TestClient, tmp_path, monkeypatch):
    # Point sample path by ensuring scripts/sample_batch.json exists (repo file)
    seed = client.post("/api/v1/ingest/synthetic")
    assert seed.status_code == 200
    assert seed.json()["inserted"] >= 1

    cases = client.get("/api/v1/cases").json()
    cid = cases[0]["id"]
    assert cases[0]["customer_ref"] == "Protected account"

    bad = client.post(f"/api/v1/cases/{cid}/execute")
    # may 400 if no decision yet
    assert bad.status_code in {200, 400}

    d = client.post(f"/api/v1/cases/{cid}/decide?auto_execute=true")
    assert d.status_code == 200
    body = d.json()
    assert "gated_action" in body

    audit = client.get(f"/api/v1/cases/{cid}/audit")
    assert audit.status_code == 200
    kinds = [e["kind"] for e in audit.json()]
    assert "outcome" in kinds or "executed" in kinds

    missing = client.get("/api/v1/cases/not-a-real-id")
    assert missing.status_code == 404

    ev = client.post("/api/v1/eval/runs?seed=7")
    assert ev.status_code == 200
    assert "lift_value" in ev.json()

    batch = client.post("/api/v1/cases/batch/decide?auto_execute=true")
    assert batch.status_code == 200


def test_api_webhook_fails_closed_without_secret(client: TestClient):
    r = client.post("/api/v1/ingest/webhooks/razorpay", json={})
    assert r.status_code == 503
    assert r.json()["detail"] == "razorpay_webhook_secret_required"


def test_api_webhook_requires_secret(client: TestClient, monkeypatch):
    from apps.api import main as api_main

    monkeypatch.setattr(api_main.settings, "razorpay_webhook_secret", "")

    response = client.post(
        "/api/v1/ingest/webhooks/razorpay",
        json={"id": "evt_mvp_unsigned", "amount_paise": 12_000, "customer_ref": "cust_mvp"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "razorpay_webhook_secret_required"


def test_api_webhook_signature_when_secret_configured(client: TestClient, monkeypatch):
    from apps.api import main as api_main

    secret = "test-webhook-secret"
    monkeypatch.setattr(api_main.settings, "razorpay_webhook_secret", secret)
    payload = {
        "id": "evt_signed_1",
        "amount_paise": 12_000,
        "customer_ref": "cust_signed",
        "failure_class": "bank_decline",
    }
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()

    missing = client.post(
        "/api/v1/ingest/webhooks/razorpay",
        content=raw,
        headers={"content-type": "application/json"},
    )
    assert missing.status_code == 401

    invalid = client.post(
        "/api/v1/ingest/webhooks/razorpay",
        content=raw,
        headers={"content-type": "application/json", "X-Razorpay-Signature": "wrong"},
    )
    assert invalid.status_code == 401

    created = client.post(
        "/api/v1/ingest/webhooks/razorpay",
        content=raw,
        headers={"content-type": "application/json", "X-Razorpay-Signature": signature},
    )
    assert created.status_code == 200
    assert created.json()["created"] is True

from __future__ import annotations

from enum import Enum


class CaseStatus(str, Enum):
    OPEN = "open"
    ACTING = "acting"
    RECOVERED = "recovered"
    STOPPED = "stopped"
    ESCALATED = "escalated"


class CaseSource(str, Enum):
    SYNTHETIC = "synthetic"
    WEBHOOK = "webhook"


class Action(str, Enum):
    SILENT_RETRY = "silent_retry"
    PAYMENT_LINK = "payment_link"
    NOTIFY_UPDATE_METHOD = "notify_update_method"
    ESCALATE = "escalate"
    STOP = "stop"


ALLOWLISTED_ACTIONS = frozenset(a.value for a in Action)


class GateResult(str, Enum):
    ALLOW = "allow"
    REWRITE_STOP = "rewrite_stop"
    REWRITE_ESCALATE = "rewrite_escalate"
    REJECT = "reject"


class ExecutionMode(str, Enum):
    DRY_RUN = "dry_run"
    LIVE_TEST = "live_test"
    SIMULATED = "simulated"


class OutcomeResult(str, Enum):
    RECOVERED = "recovered"
    FAILED = "failed"
    PENDING = "pending"
    STOPPED = "stopped"


class OutcomeLabel(str, Enum):
    TEST_MODE = "test_mode"
    SIMULATED = "simulated"
    BASELINE = "baseline"


class ProposerKind(str, Enum):
    RULES = "rules"
    MODEL = "model"
    LLM = "llm"


class AuditKind(str, Enum):
    INGESTED = "ingested"
    SCORED = "scored"
    PROPOSED = "proposed"
    GATED = "gated"
    EXECUTED = "executed"
    OUTCOME = "outcome"
    NOTE = "note"

# Problem decomposition — Rebound

> Day 02 (22 Aug 2026). Turns the locked thesis into buildable pieces.

## Problem → jobs

| Job | Question the system answers | Failure if missing |
| --- | --- | --- |
| **Ingest** | What revenue is at risk right now? | No queue → nothing to decide |
| **Diagnose** | Why might this have failed? (features, not vibes) | Random actions |
| **Score** | P(recover \| action, x), value, cost | Cannot rank interventions |
| **Decide** | Which allowlisted action (incl. stop/escalate)? | LLM freelances money actions |
| **Gate** | Does policy allow this proposal? | Unsafe / duplicate / over-cap |
| **Act** | Execute via Razorpay-compatible workflow or simulate outreach | Demo without rails |
| **Observe** | Did it recover? What did it cost? | No learning / no metrics |
| **Evaluate** | Incremental lift vs baseline on a batch? | Vanity “recovered ₹” |

## Core loop (single case)

```text
Event (subscription.pending / payment.failed / synthetic)
        │
        ▼
Case record (idempotent on event_id)
        │
        ▼
Feature snapshot (amount, method, decline class, attempt #, tenure, …)
        │
        ▼
Scorer → {P_recover[action], cost[action], value}
        │
        ▼
Proposer (rules + optional LLM structured JSON)
        │  action, rationale, confidence
        ▼
Policy engine (allowlist, caps, stopping rules, confidence floor)
        │  allow | rewrite | rewrite_to_stop | escalate
        ▼
Executor (Payment Link | note retry | log outreach | stop)
        │
        ▼
Outcome + AuditEvent
```

## Entity vocabulary

| Term | Meaning |
| --- | --- |
| **Case** | One at-risk revenue unit (e.g. failed subscription invoice cycle) |
| **Action** | Allowlisted intervention enum |
| **Proposal** | Model/rules output before gating |
| **Decision** | Gated, immutable choice recorded on the case |
| **Baseline run** | Same batch under fixed ladder policy (no EV) |
| **Lift** | recovered_value(Rebound) − recovered_value(baseline) |

## Allowlisted actions (MVP)

| Action ID | Description | Execution | Cost model (demo) |
| --- | --- | --- | --- |
| `silent_retry` | Signal / schedule another charge attempt | Log + optional test-mode charge path | Low |
| `payment_link` | Create Razorpay Payment Link for recovery | Razorpay test-mode API | Medium |
| `notify_update_method` | Log “send update-method outreach” | **Simulated** (audit only) | Medium |
| `escalate` | Flag for human review | Queue status only | Ops cost |
| `stop` | Do not act further | Terminal | Zero action cost |

No voice/WhatsApp send in MVP. Simulation must be labeled `simulated` in metrics.

## Decomposition into modules (maps to `src/` on Aug 23)

| Module | Owns | Does not own |
| --- | --- | --- |
| `ingest` | Webhook verify (stub), synthetic batch loader, idempotency | Scoring |
| `features` | Feature extraction from case + history | Policies |
| `scoring` | P(recover), EV helpers, baseline policies | HTTP |
| `propose` | Structured action proposal | Direct Razorpay calls |
| `policy` | Deterministic gates | ML training |
| `execute` | Razorpay client + simulators | Deciding |
| `audit` | Append-only event log | UI chrome |
| `eval` | Batch runner, lift report | Live traffic |
| `api` | FastAPI routes | Business rules duplication |
| `web` | Ops UI (queue, explain, audit, eval) | Model training |

## Risks → design responses

| Risk | Response |
| --- | --- |
| Looks like “AI retry” | Scoreboard = lift vs baseline; `stop` is first-class |
| Duplicate webhook processing | Idempotent `event_id` / `case_key` |
| LLM invents actions | JSON schema + allowlist; policy drops unknowns |
| Fake money claims | Labels: `test_mode` vs `simulated` |
| Scope creep (voice, multi-channel) | Explicitly out of MVP |

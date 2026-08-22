# 03 — Architecture

> **Status: Locked for MVP — 22 Aug 2026**  
> Detail lives in [`architecture/`](../architecture/README.md).

## High-level

```text
Razorpay test-mode / synthetic
        ↓ ingest (idempotent)
Case + features
        ↓ score EV
Proposal (rules | model | optional LLM JSON)
        ↓ deterministic policy gate
Executor (Payment Link | dry-run | simulated notify | stop)
        ↓
Outcome + append-only audit
        ↓
Eval: Rebound vs Baseline A → lift
        ↓
Ops UI (React)
```

## Components

| Component | Responsibility | Tech |
| --- | --- | --- |
| API | Ingest, decide, execute, eval | FastAPI |
| Scorer / proposer | P(recover), EV, structured proposal | sklearn/logistic + rules; optional LLM |
| Policy engine | Allowlist, caps, stop/escalate | Pure Python |
| Executor | Razorpay Payment Links + simulators | razorpay SDK / HTTP |
| Store | Cases, decisions, audit, eval | SQLite (+ SQLAlchemy) |
| Web | Queue, explain, audit, eval | React + TypeScript |

## Data flow

1. Event or batch row → upsert `Case`  
2. Build features → score actions  
3. Propose allowlisted action  
4. Gate → Decision  
5. Execute (mode: dry_run / test_mode / simulated)  
6. Record Outcome + AuditEvent  
7. Batch EvalRun computes **lift_value**

## Key design decisions

See [`architecture/ADRs.md`](../architecture/ADRs.md) (SQLite, mandatory policy, no agent framework, Payment Link primary, simulated outreach, baseline-first eval).

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Thesis collapses to “AI retry” | Lift vs baseline; `stop` first-class; diff doc |
| Duplicate side effects | Idempotency keys on events + attempts |
| LLM unsafe actions | No direct tool access; schema + policy |
| Dishonest metrics | `test_mode` vs `simulated` labels |
| Slip schedule | MVP scope freeze file |

## Non-goals (architecture)

- Microservices, queues, multi-tenant SaaS polish  
- Live messaging providers in MVP  
- Recreating Razorpay Intelligent Retry / Agent Studio  

## MVP freeze

[`architecture/mvp-scope.md`](../architecture/mvp-scope.md)

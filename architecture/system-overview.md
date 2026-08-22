# System overview

> Rebound architecture — locked for MVP build start (22 Aug 2026).

## Context diagram

```text
┌─────────────┐     webhook / synthetic      ┌──────────────────┐
│  Razorpay   │ ───────────────────────────▶ │   Rebound API    │
│  test-mode  │ ◀── Payment Links / reads ── │    (FastAPI)     │
└─────────────┘                              └────────┬─────────┘
                                                      │
                 ┌────────────────────────────────────┼────────────────────────┐
                 │                                    ▼                        │
                 │  ingest → features → score → propose → policy → execute     │
                 │                         │                │                  │
                 │                         ▼                ▼                  │
                 │                      audit DB ←──────── outcomes            │
                 │                         │                                   │
                 │                         ▼                                   │
                 │                      eval runner                            │
                 └─────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
                                              ┌───────────────┐
                                              │  Ops UI       │
                                              │  (React/TS)   │
                                              └───────────────┘
```

## Sequence — decide & act

```mermaid
sequenceDiagram
  participant Src as Webhook/Synthetic
  participant API as FastAPI
  participant Pol as Policy
  participant RZ as Razorpay test-mode
  participant DB as SQLite

  Src->>API: event / batch row
  API->>DB: upsert Case (idempotent)
  API->>API: features + score EV
  API->>API: propose action
  API->>Pol: gate(proposal)
  alt allow payment_link
    Pol->>API: allow
    API->>RZ: create Payment Link
    RZ-->>API: link id/url
    API->>DB: ActionAttempt + Audit
  else stop / escalate / simulate notify
    Pol->>API: allow rewritten or stop
    API->>DB: ActionAttempt (simulated/dry_run) + Audit
  end
  API->>DB: Outcome (when known)
```

## Safety architecture (non-negotiable)

```text
ML / rules / optional LLM
        ↓  structured proposal only
Deterministic policy engine
        ↓  allowlist + caps + stop rules
Executor (Razorpay client | simulator)
        ↓
Audit trail
```

The LLM never calls Razorpay directly.

## Package layout (Aug 23 target)

```text
src/
  apps/
    api/                 # FastAPI entry
    web/                 # React app
  rebound/
    ingest/
    features/
    scoring/
    propose/
    policy/
    execute/
    audit/
    eval/
    db/
    schemas/
  scripts/
    seed_batch.py
    run_eval.py
```

## Runtime config

| Var | Purpose |
| --- | --- |
| `RAZORPAY_KEY_ID` / `SECRET` | Test-mode |
| `RAZORPAY_WEBHOOK_SECRET` | Optional verify |
| `REBOUND_EXECUTION_MODE` | `dry_run` \| `test_mode` |
| `REBOUND_ENABLE_LLM_PROPOSER` | default `false` |
| `DATABASE_URL` | sqlite:///./rebound.db |

## Non-goals (architecture)

- Microservice mesh  
- Event bus / Kafka  
- Multi-region  
- Replacing Razorpay retry rails  

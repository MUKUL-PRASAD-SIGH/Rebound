# Data model (MVP)

> SQLite-first. Postgres-compatible types preferred in SQLAlchemy models later.

## ER (logical)

```text
Merchant (demo singleton)
    │
    ├── Case ──────────────────── AuditEvent
    │     │
    │     ├── Proposal
    │     ├── Decision
    │     └── ActionAttempt ─── Outcome
    │
    └── EvalRun ── EvalCaseResult
```

## Tables

### `cases`
| Column | Type | Notes |
| --- | --- | --- |
| id | UUID/text PK | |
| case_key | text unique | Stable idempotency key |
| source | text | `synthetic` \| `webhook` |
| external_event_id | text null unique | Razorpay event id when present |
| status | text | `open` \| `acting` \| `recovered` \| `stopped` \| `escalated` |
| amount_paise | int | |
| currency | text | default INR |
| customer_ref | text | opaque demo id |
| failure_code | text null | |
| failure_class | text | e.g. `insufficient_funds`, `expired_card`, `unknown` |
| attempt_n | int | |
| tenure_days | int | |
| method | text | upi/card/… |
| payload_json | text/json | raw |
| created_at / updated_at | datetime | |

### `proposals`
| Column | Notes |
| --- | --- |
| id, case_id | |
| action | allowlisted enum |
| confidence | 0–1 |
| ev | float |
| p_recover | float |
| rationale | text |
| proposer | `rules` \| `model` \| `llm` |
| created_at | |

### `decisions`
| Column | Notes |
| --- | --- |
| id, case_id, proposal_id null | |
| action | final gated action |
| gate_result | `allow` \| `rewrite_stop` \| `rewrite_escalate` \| `reject` |
| gate_reason | text |
| policy_version | text |
| created_at | |

### `action_attempts`
| Column | Notes |
| --- | --- |
| id, case_id, decision_id | |
| action | |
| mode | `live_test` \| `dry_run` \| `simulated` |
| request_json / response_json | |
| razorpay_payment_link_id | null |
| idempotency_key | unique |
| created_at | |

### `outcomes`
| Column | Notes |
| --- | --- |
| id, case_id, action_attempt_id null | |
| result | `recovered` \| `failed` \| `pending` \| `stopped` |
| value_paise | |
| label | `test_mode` \| `simulated` \| `baseline` |
| observed_at | |

### `audit_events`
Append-only. `id, case_id, kind, payload_json, created_at`  
Kinds: `ingested`, `scored`, `proposed`, `gated`, `executed`, `outcome`, `note`

### `eval_runs` / `eval_case_results`
Store batch id, policy name (`baseline_a` \| `rebound`), per-case action + outcome, aggregates JSON.

## Idempotency rules

1. Webhook/`external_event_id` → upsert case, never double-open  
2. `action_attempts.idempotency_key` = `case_id + action + decision_id`  
3. Re-running eval creates a **new** `eval_run`, does not mutate historical audits  

## Feature vector (v1)

Used by scorer (stored optionally as JSON on case or derived on the fly):

- `amount_paise`, `log_amount`
- `attempt_n`, `tenure_days`
- `failure_class` (one-hot)
- `method` (one-hot)
- `days_since_last_success` (synthetic ok)
- `prior_recoveries`, `prior_stops` (synthetic ok)

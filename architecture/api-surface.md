# API surface (MVP)

Base: `/api/v1`

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Liveness |
| POST | `/ingest/synthetic` | Upload/seed batch |
| POST | `/ingest/webhooks/razorpay` | Webhook-shaped events |
| GET | `/cases` | List / filter |
| GET | `/cases/{id}` | Detail + latest decision |
| POST | `/cases/{id}/decide` | Run propose→gate→(optional execute) |
| POST | `/cases/{id}/execute` | Execute last allowed decision |
| GET | `/cases/{id}/audit` | Audit trail |
| POST | `/eval/runs` | Run Baseline A + Rebound on batch |
| GET | `/eval/runs/{id}` | Aggregates + lift |
| GET | `/metrics/summary` | Dashboard counters |

## Proposal JSON schema (LLM/rules)

```json
{
  "action": "silent_retry | payment_link | notify_update_method | escalate | stop",
  "confidence": 0.0,
  "p_recover": 0.0,
  "ev": 0.0,
  "rationale": "short string"
}
```

Unknown `action` → policy rewrites to `stop` and audits `reject_unknown_action`.

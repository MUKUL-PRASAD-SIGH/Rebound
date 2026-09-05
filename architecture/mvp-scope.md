# MVP scope — freeze (22 Aug 2026)

> If it is not in this file, it does not ship in the Aug 26 MVP.

## MVP goal

**Ugly but working** end-to-end loop:

1. Load a batch of at-risk cases (synthetic + optional webhook-shaped JSON)  
2. Run **Baseline A** and **Rebound** on the same batch  
3. For Rebound cases: propose → gate → execute (Payment Link and/or simulated notify)  
4. Show ops UI: queue, decision reason, audit trail  
5. Show eval panel: recovery rate, estimated cost, **incremental lift**

## In scope (Aug 23–26)

| Area | Must have |
| --- | --- |
| Backend | FastAPI app boots; health route; CRUD-ish case APIs |
| DB | SQLite OK for speed (swap later if needed) |
| Ingest | Synthetic CSV/JSON batch (≥50 cases for Track-03-style bar) |
| Ingest | Webhook endpoint accepting Razorpay-*shaped* payloads (signature verify can be stubbed with flag) |
| Scoring | Heuristic + simple sklearn/XGBoost-or-logistic model trained on synthetic labels |
| Propose | Deterministic proposer using EV; optional LLM proposer behind flag (structured JSON only) |
| Policy | Allowlist, max retries, max notifies, min EV, confidence floor, force-stop rules |
| Execute | Create Payment Link in **MVP mode (Razorpay Test Mode)** when configured; else dry-run executor |
| Execute | `notify_update_method` / outreach = simulated log |
| Audit | Every proposal/gate/execute/outcome appended |
| Eval | Batch job comparing Baseline A vs Rebound |
| UI | React pages: Cases, Case detail (explain), Audit, Eval report |
| Config | `.env` from `.env.example`; no secrets in git |

## Out of scope (MVP)

- Live WhatsApp / voice / ElevenLabs  
- Cloning Agent Studio UX  
- Replacing Razorpay Intelligent Retry  
- Production deploy hardening (beyond a free/simple host if time)  
- Real merchant money / live mode keys  
- Graph fraud / chargeback products  
- Multi-tenant auth beyond a simple demo lock (optional basic password later)  
- LangGraph/CrewAI framework maze  

## Stretch (only after Aug 26 if MVP green)

- Checkout abandonment cases  
- Baseline B (always aggressive)  
- Real webhook signature verification  
- Calibrated probabilities + reliability plots  
- Human approval gate for high-value cases  

## Definition of Done — Aug 26

- [ ] `docker`/local one-command or documented `make`/`scripts` run  
- [ ] Seed batch → Rebound decisions visible in UI  
- [ ] At least one Payment Link created in MVP mode (Razorpay Test Mode) **or** explicit dry-run mode with screenshot
- [ ] Eval page shows lift (even if lift ≤ 0 — honest)  
- [ ] Audit trail for a single case shows proposal → gate → action → outcome  
- [ ] README “Run locally” section filled  

## Success metrics (batch demo)

| Metric | Definition |
| --- | --- |
| `recovery_rate` | `# recovered / # cases` |
| `recovered_value` | Sum of case values marked recovered |
| `intervention_cost` | Sum of action costs (configured table) |
| `net_value` | `recovered_value - intervention_cost` |
| **`lift_value`** | `net_value(Rebound) - net_value(Baseline A)` |
| `stop_rate` | Share of cases ending in `stop` without further action |
| `escalation_rate` | Share sent to `escalate` |
| `simulated_share` | Share of recoveries labeled simulated (must be visible) |

Primary headline metric: **`lift_value`** (and honesty about simulation).

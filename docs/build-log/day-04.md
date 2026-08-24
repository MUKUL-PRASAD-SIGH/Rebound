# Day 04 — 24 Aug 2026

## Goal
Core happy-path workflow (no ML yet): ingest → decide (rules ladder) → policy gate → dry_run/simulated execute → audit visible in UI.

## What I did
- `rebound/propose`: rules ladder proposer (`silent_retry` → `payment_link` → `notify` → `stop` / escalate)
- `rebound/policy`: allowlist + confidence floor + retry/notify caps + high-value escalate rewrite
- `rebound/execute`: dry_run / simulated outreach executors (safe by default)
- `rebound/workflow.py`: orchestrates propose → gate → optional execute + audit events
- `rebound/ingest`: webhook-shaped upsert (signature verify still stubbed)
- API: real `POST /cases/{id}/decide`, `POST /cases/{id}/execute`, webhook ingest returns case
- UI: Case detail — Decide / Decide+execute / Execute latest + live audit table
- Smoke test: `silent_retry → allow → executed`

## Decisions
- Day 04 stays rules-only; EV/sklearn is Day 05
- Default execution remains `dry_run` / `simulated` (no live Razorpay side effects required)
- Eval batch runner still stubbed (Day 05/06)

## Problems
- None blocking

## Experiments
- Local Python smoke: decide_case(auto_execute=True) on seeded case → allow + execute

## Evidence
- `src/rebound/workflow.py`, `propose/`, `policy/`, `execute/`, `ingest/`
- `src/apps/web/src/pages/CaseDetailPage.tsx`
- This log + BUILD_LOG Day 04

## Done for Day 04
- [x] Rules decide path  
- [x] Policy gate with caps  
- [x] Dry_run / simulated execute  
- [x] Audit trail on decide/execute  
- [x] Case detail UI wired  
- [x] Webhook-shaped ingest upsert  
- [x] Day log + push  

## Stop line
**Day 04 ends here.** No eval lift runner / no ML model training in this day.

## Next (Day 05 — Intelligence)
- EV scorer / simple model + richer propose
- Batch eval scaffolding toward `lift_value`

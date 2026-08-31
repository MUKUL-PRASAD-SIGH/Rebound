# Day 06 — 26 Aug 2026

## Goal
Integration: end-to-end MVP with batch eval (Baseline A vs Rebound) and UI surface for `lift_value`.

## What I did
- `rebound/eval`: Baseline A / Baseline B / Rebound policy sims → aggregates + honest simulated label
- API: `POST/GET /api/v1/eval/runs`, list runs
- UI: Eval page (run + past lifts); Home copy updated for EV loop
- Script: `run_eval.py` (local or `--api`)

## Decisions
- Headline metric stays `lift_value = net(Rebound) - net(Baseline A)` with `simulated_net_value_delta` label
- Recoveries simulated from scored probabilities — never claim real ₹
- MVP “ugly but working” closes with decide → execute → eval loop

## Problems
- None blocking

## Experiments
- Local `run_eval` on seeded cases returns policies + lift

## Evidence
- `src/rebound/eval/__init__.py`
- `src/apps/web/src/pages/EvalPage.tsx`
- API routes in `main.py`

## Done for Day 06
- [x] Eval runner + persistence  
- [x] Eval API  
- [x] Eval UI  
- [x] MVP end-to-end path  

## Next (Day 07+)
- Iteration: batch decide, global audit, baselines in UI, tests

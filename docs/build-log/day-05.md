# Day 05 — 25 Aug 2026

## Goal
Intelligence layer: EV scoring + recoverability model + EV-max proposer (rules ladder retained as fallback).

## What I did
- `rebound/features`: vectorize case features (log amount, attempt, tenure, failure/method one-hots)
- `rebound/scoring`: logistic recoverability model, **proportional** action costs, failure-class multipliers, `score_actions` / EV
- `rebound/propose`: default `propose_ev` with attempt bans + relative EV floor (so stop / link / notify appear — not 60× payment_link)
- `rebound/policy`: `min_ev` gate rewrite to stop
- Scripts: `generate_batch.py` (60 cases, includes ≥500k for escalate demos), `train_model.py` → `recover_model.json` (gitignored; regenerate locally)
- Docs: [`docs/EXTERNAL_REQUIREMENTS.md`](../EXTERNAL_REQUIREMENTS.md) — external tools/APIs checklist

## Decisions
- Prefer EV-max over rules for live decide; rules remain for Baseline A / fallback
- Persist model as JSON coefs (no pickle); artifact gitignored
- Costs scale with amount so EV ranking is meaningful
- Synthetic labels derived from heuristic family — honest for demo, not production lift

## Problems
- Windows console encoding broke unicode arrows in script prints — switched to `->`
- Early EV costs were too small → degenerate always-link proposals — fixed with proportional costs + attempt bans

## Experiments
- Train synthetic logistic on 800 rows; propose_ev returns diverse actions across failure/attempt mixes

## Evidence
- `src/rebound/scoring/`, `features/`, `propose/`, `policy/`
- `src/scripts/sample_batch.json` (60)
- `docs/EXTERNAL_REQUIREMENTS.md`

## Done for Day 05
- [x] Feature vector + EV scorer  
- [x] Model train/save/load  
- [x] EV proposer wired as default  
- [x] Larger synthetic batch (≥50, high-value included)  
- [x] External requirements single MD  

## Next (Day 06)
- Eval runner: Baseline A vs Rebound → `lift_value` API + UI (paired RNG)
- Outcome recording + re-open ladder

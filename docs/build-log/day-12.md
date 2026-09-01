# Day 12 — 1 Sep 2026 (today, commit 3 of 3)

## Goal
Evaluation depth: sensitivity + second seed runs.

## What I did
- Documented re-run with alternate seeds via `run_eval(seed=…)`
- Noted that lift can flip sign under different RNG — judges must see sim share
- Makefile / scripts path for one-command local eval

## Decisions
- Report variance qualitatively in evidence; do not cherry-pick a single lucky seed in README claims
- Keep Baseline A as primary comparator

## Evidence
- `evidence/benchmarks/sensitivity.md`

## Done
- [x] Sensitivity notes
- [x] Repro commands

## Next
- Day 13 differentiation polish (Sep 2, tomorrow, push 1 of 3)

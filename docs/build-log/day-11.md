# Day 11 — 1 Sep 2026 (today, shared commit 2 of 3)

## Goal
Serious evaluation: document benchmarks + edge cases.

## What I did
- `evidence/benchmarks/README.md` — how to reproduce lift runs
- Edge-case notes: zero EV stop, max retries, high-value escalate, empty batch 400
- Seeded 60-case batch as default eval corpus

## Decisions
- Treat synthetic recoveries as **upper-bound demo signal**, not merchant ROI claim
- Always publish `lift_value_label` with the number

## Evidence
- `evidence/benchmarks/`
- `src/scripts/sample_batch.json`

## Done
- [x] Benchmark reproduction notes
- [x] Edge-case checklist

## Next
- Day 12 sensitivity notes (Sep 1, commit 3 of 3)

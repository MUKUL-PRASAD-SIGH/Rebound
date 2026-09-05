# Day 14 — 2 Sep 2026 (today, commit 2 of 3)

## Goal
Polish + deployment ergonomics (local demo-ready).

## What I did
- Root `Makefile` for API, web, seed helpers, eval, and tests
- `README.md` with Make and Windows-friendly manual start paths
- Confirmed default modes remain dry_run / simulated

## Decisions
- Local demo is the submission path; Docker optional later if time
- Never require live Razorpay keys for core demo

## Evidence
- `Makefile`, `README.md`

## Done
- [x] One-command docs for demo

## Next
- Day 15 submission package (Sep 2, commit 3 of 3); then protect Sep 3 for full testing

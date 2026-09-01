# Day 10 — 1 Sep 2026 (today, shared commit 2 of 3)

## Goal
Close iteration week with regression tests.

## What I did
- `src/tests/test_core.py`: scoring, policy, rules ladder, eval lift smoke
- pytest against in-memory SQLite

## Decisions
- Prefer cheap unit tests over brittle full browser E2E for buildathon pace
- Eval test asserts structure + label honesty, not a fixed lift number

## Evidence
- `src/tests/test_core.py`

## Done
- [x] Core test suite

## Next
- Day 11 benchmark notes ship in this shared commit; Day 12 sensitivity follows in commit 3 of 3

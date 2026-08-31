# Day 08 — 28 Aug 2026

## Goal
Iteration: Baseline B in eval aggregates + clearer policy comparison in UI.

## What I did
- Eval already includes Baseline B (`notify`/`link` heuristic) alongside A and Rebound
- Eval UI table shows all policies (recovery rate, net, cost, stop rate, sim share)
- Honest note surfaced in UI

## Decisions
- Keep three policies in one run for judges: fixed ladder (A), alternate heuristic (B), EV Rebound
- Do not invent “live” lift — label stays simulated

## Evidence
- `EvalPage.tsx`, `rebound/eval`

## Done
- [x] Baseline B in runner + UI

## Next
- Approval / escalate UX + edge-case hardening

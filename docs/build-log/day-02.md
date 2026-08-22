# Day 02 — 22 Aug 2026

## Goal
Problem decomposition + architecture + MVP scope freeze for Rebound (no feature coding yet).

## What I did
- Wrote problem decomposition (jobs, loop, modules, allowlisted actions)
- Froze MVP in/out + Aug 26 Definition of Done + batch metrics
- System overview diagrams + safety architecture
- Data model + API surface
- ADRs 001–007 (SQLite, policy mandatory, no agent framework, Payment Link primary, simulated outreach, baseline-first eval, dual proposer)
- Locked baseline policy knobs for eval
- Updated living `docs/03-architecture.md` and project overview stack

## Decisions
- SQLite for MVP; SQLAlchemy-friendly
- Payment Link = primary real Razorpay side effect
- Outreach simulated + labeled
- Rules/EV proposer default; LLM optional behind flag
- Headline metric = `lift_value` vs Baseline A
- Aug 23 starts `src/` skeleton per package layout

## Problems
- None blocking; sandbox subscription quirks deferred to executor dry-run fallback

## Experiments
- None (design day)

## Evidence
- `architecture/` (README, decomposition, mvp-scope, system-overview, data-model, api-surface, ADRs)
- `docs/03-architecture.md`
- `research/15-baseline-policies-draft.md`

## Tomorrow (Aug 23 — Skeleton)
- ~~Create `src/apps/api` + `src/rebound/*` package stubs~~ → **Done (Day 03)**
- ~~DB models + health route~~ → **Done**
- ~~React app shell + seed~~ → **Done**
- See [`day-03.md`](./day-03.md)

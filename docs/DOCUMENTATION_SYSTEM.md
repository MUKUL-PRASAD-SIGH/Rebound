# Documentation System

This repo uses a **3-layer** evidence workflow for the Razorpay Buildathon.

**Calendar:** see root [`SCHEDULE.md`](../SCHEDULE.md) — 2 days research/design, then heavy build/iterate. After Aug 22, research only for concrete implementation questions.

## Layers

| Layer | Where | Cadence | Audience |
| --- | --- | --- | --- |
| Laboratory notebook | This private repo | Daily | You (future you + judges' proof trail) |
| Edited documentary | Medium drafts → publish | Milestones only (3–5 articles) | Readers / community |
| Engineering artifact | Public GitHub (later) | Near submission | Judges / recruiters |

**Rule:** document daily, publish selectively. Never rewrite old build-log entries.

## What goes where

### Daily (mandatory, ~5–10 min)

1. Create / update `docs/build-log/day-NN.md`
2. Append the same day to root `BUILD_LOG.md` (never edit past days)
3. Drop screenshots / benchmarks into `evidence/…` with date prefixes

### Living docs (update when reality changes)

| File | Purpose |
| --- | --- |
| `00-project-overview.md` | What / why / for whom (filled after PS chosen) |
| `01-research.md` | Summary + pointer into deep research |
| `02-ideation.md` | Ideas considered, chosen direction |
| `03-architecture.md` | System design (current truth) |
| `04-development-log.md` | Curated summary of build phases |
| `05-experiments.md` | Experiments + outcomes |
| `06-evaluation.md` | Metrics, benchmarks, failure modes |
| `07-final-results.md` | Final narrative for submission week |

### Deep research (problem-solving before code)

Root folder [`research/`](../research/README.md) is the living investigation across all five tracks: landscape, contemporary developments, rejected ideas, comparison, provisional selection. Judges/readers should be able to follow the thinking without assuming the answer was obvious.

### Medium (do not post daily)

Draft in `docs/medium-drafts/`. Suggested milestone set:

1. **The Beginning** — who / why / research / hypothesis
2. **Building V1** — stack, first prototype, early failures
3. **What Went Wrong** — pivot story with evidence
4. **The Final Build** — polished case study + demo + GitHub

Opening tone (personal journey, not CV dump):

> Hey, I'm Mukul. … For the Razorpay Buildathon, I decided to document the entire journey — not just the final product. … Let's see where this goes.

Then jump into: **Day 0 — Finding the Problem**.

## Evidence naming

```text
evidence/screenshots/YYYY-MM-DD_short-label.png
evidence/benchmarks/YYYY-MM-DD_run-name.md
evidence/experiments/YYYY-MM-DD_experiment-name.md
evidence/iterations/YYYY-MM-DD_vN-notes.md
```

## Git commit style

Prefer proof-of-work commits:

```text
feat: …
fix: …
refactor: …
experiment: …
test: …
docs: …
chore: …
```

Avoid: `final changes`, `updates`, `wip` as the only message forever.

## Publication gate (near submission)

Private lab → curate strongest evidence → public README + Medium + demo video.

Check Buildathon rules before flipping the repo to public.

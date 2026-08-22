# Build Log

Append-only. Never rewrite past days. Detailed day files also live in `docs/build-log/`.

---

## 21 August 2026 — Day 00 (setup)

### Goal
Define the private documentation / evidence structure before choosing a problem statement.

### What I built
- Repo skeleton: `docs/`, `evidence/`, `architecture/`, `src/`
- Numbered living docs (`00`–`07`)
- Daily build-log system + this append-only `BUILD_LOG.md`
- `.gitignore` + `.env.example` (secrets stay out)
- `DOCUMENTATION_SYSTEM.md` (3-layer: private lab → Medium milestones → public artifact)

### What failed
- N/A (setup day)

### Decisions
- Keep repo **private** until submission-ready
- Document daily; publish Medium only on milestones (not daily posts)
- Problem statement selection is the **next** step — structure first so evidence starts clean

### Evidence
- Structure itself in this commit / working tree

### Next
- Choose problem statement (PS)
- Fill `docs/01-research.md` shortlist + `docs/02-ideation.md`
- Lock working title in `docs/00-project-overview.md`

---

## 21 August 2026 — Day 01 (research across all tracks)

### Goal
Understand all five buildathon tracks in the context of what Razorpay already builds — before coding.

### What I built
- Living research system under `research/` (context → tracks → landscape → comparison → rejected ideas → provisional selection)
- Updated `docs/01-research.md` and `docs/02-ideation.md` as summaries
- Source ledger in `research/sources.md`

### What failed / what died
- Naive "AI retry agent" (retries + Intelligent Retry + Subscription Recovery already exist)
- Chat-checkout clone (Agentic Payments / Reserve Pay / brand pilots)
- Generic fraud classifier & dispute-bot clone (Vulcan/SHIELD/Agent Studio overlap)

### Decisions
- Leading provisional thesis: Track 03 expected-value recovery decision layer
- Not locked until test-mode path + differentiation sentence are verified
- Track 01 conditional; Track 04 backup; Track 02/05 parked

### Evidence
- `research/README.md` and files 00–12

### Next
- **Tonight / rest of Aug 21:** lock PS thesis (stop open-ended research)
- **Aug 22:** problem decomposition + architecture + MVP scope (`SCHEDULE.md`)
- Claude / NotebookLM / Gemini only if they answer a concrete question — do not burn the build calendar
- **Aug 23:** start skeleton in `src/`

---

## Schedule lock (same day)

Adopted 15-day build-heavy calendar in [`SCHEDULE.md`](SCHEDULE.md):

- Research/design: Aug 21–22 only (2 days)
- MVP build: Aug 23–26 (ugly but working)
- Continuous testing during build; serious eval Aug 31–Sep 1
- Submit Sep 5

Rule after Aug 22: **research only when it answers a concrete implementation question.**

---

## 21 August 2026 — Day 01 close-out (PS locked)

### Goal
Complete Aug 21 deliverable: **Final PS + research notes**.

### What I built / locked
- **Track 03 — AI Revenue Recovery**
- Project name: **Rebound**
- Thesis: expected-value decision layer above Razorpay recovery rails (not “AI retry”)
- Docs: `research/12`–`15`, `docs/00-project-overview.md`, ideation/research summaries
- Differentiation one-pager vs Agent Studio Subscription Recovery
- Draft baselines for evaluation

### Decisions
- PS selection research is **closed**
- Aug 22 = architecture + MVP scope only
- Extra AI tool passes deferred unless they unblock a concrete build question

### Evidence
- `research/12-final-selection.md` (LOCKED)
- `docs/00-project-overview.md`
- `SCHEDULE.md`

### Next (Aug 22)
- Decompose Rebound into components
- Architecture + MVP in/out
- Ready `src/` skeleton for Aug 23

---

## 22 August 2026 — Day 02 (architecture + MVP freeze)

### Goal
Turn Rebound into a buildable system design without writing product features yet.

### What I built
- `architecture/problem-decomposition.md` — jobs, loop, modules, actions
- `architecture/mvp-scope.md` — in/out freeze, Aug 26 DoD, metrics
- `architecture/system-overview.md` — diagrams + safety + package layout
- `architecture/data-model.md` + `api-surface.md`
- `architecture/ADRs.md` — seven decisions (SQLite, policy gate, no agent framework, …)
- Updated `docs/03-architecture.md`, overview stack lock, baselines

### Decisions
- Headline metric: `lift_value` vs Baseline A
- Payment Link = primary test-mode side effect; outreach simulated
- Rules/EV default proposer; LLM optional behind flag
- Aug 23 coding starts from documented package layout

### Evidence
- `architecture/README.md` and linked docs
- `docs/build-log/day-02.md`

### Next (Aug 23)
- Skeleton: FastAPI + SQLite models + React shell + seed stub

---

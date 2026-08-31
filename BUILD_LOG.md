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

## 23 August 2026 — Day 03 (skeleton)

### Goal
Repo runs with empty paths wired: API + DB + UI shell.

### What I built
- `src/rebound/` packages (db, schemas, policy/audit stubs, …)
- FastAPI: health, metrics, cases, audit, synthetic ingest; stubs for decide/execute/eval/webhook
- React/Vite ops UI (Home / Cases / Detail / Eval / Audit)
- `requirements.txt`, sample batch, seed script
- Verified: health ok, seeded 5 cases, metrics reflect counts

### Decisions
- Run API with `--app-dir src`
- Vite proxy `/api` → backend
- Decide/execute deferred to Day 04–05 (intentional stubs)

### Evidence
- Local API verification (health + ingest + cases)
- `docs/build-log/day-03.md`

### Next (Aug 24)
- Core happy-path workflow (rules ladder decide + dry_run execute + UI) — **not started; Day 03 closed**

---

## Documentation checkpoint (Day 03 close)

Day-wise logs through Day 03 are the source of truth:

| Day | Log |
| --- | --- |
| 00–03 | [`docs/build-log/`](docs/build-log/README.md) |
| Append-only | this file |

No Day 04 work in this checkpoint.

---

## 24 August 2026 — Day 04 (core workflow)

### Goal
Happy-path without ML: rules decide → policy gate → dry_run/simulated execute → audit in UI.

### What I built
- Rules ladder proposer + policy caps/rewrites
- Workflow orchestration (`rebound/workflow.py`)
- Dry_run / simulated executors
- Webhook-shaped ingest upsert
- API decide/execute live; Case detail UI with audit trail
- Smoke: `silent_retry → allow → executed`

### Decisions
- Rules-only on Day 04; EV/ML deferred to Day 05
- Default safe execution modes (no required live Razorpay calls)
- Eval lift runner still Day 05/06

### Evidence
- `docs/build-log/day-04.md`
- Local workflow smoke test

### Next (Day 05)
- Intelligence: EV scoring / simple model + eval scaffolding

---

## 25 August 2026 — Day 05 (intelligence)

### Goal
EV scoring + recoverability model + EV-max proposer; ≥50 synthetic batch.

### What I built
- Feature vectorization + sklearn logistic recoverability model
- Proportional action costs + failure-class multipliers (non-degenerate EV)
- `propose_ev` default with attempt bans + relative EV floor (stop is reachable)
- Policy `min_ev` gate
- `generate_batch.py` (60 cases, high-value ≥500k included) + `train_model.py`
- [`docs/EXTERNAL_REQUIREMENTS.md`](docs/EXTERNAL_REQUIREMENTS.md) — tools/APIs checklist
- `recover_model.json` gitignored (regenerate locally)

### Decisions
- No external API required for demo (Python + Node only)
- Razorpay / LLM keys optional and unused in dry_run

### Evidence
- `docs/build-log/day-05.md`

### Next (Day 06)
- Eval lift runner (paired RNG) + outcome recording + UI

---

## 26 August 2026 — Day 06 (eval lift)

### Goal
Integrate the end-to-end MVP with honest baseline comparison and a visible `lift_value` story.

### What I built
- `src/rebound/eval/__init__.py` — paired Baseline A / Rebound simulation with summary metrics
- `src/scripts/run_eval.py` — local eval runner for `lift_value` output and case-level outcomes
- API routes in `src/apps/api/main.py` — eval run create/list + recent audit endpoints
- Eval page in `src/apps/web/src/pages/EvalPage.tsx` — compare Baseline A vs Rebound and show outcomes
- Home / audit copy updated to reflect the decision loop and audit trail
- `src/tests/test_core.py` added for the eval workflow and core path

### Decisions
- Keep the headline metric as `lift_value = net(Rebound) - net(Baseline A)`
- Simulated outcomes remain explicitly labeled; never represent test-mode results as real revenue
- The MVP closes with decide → execute → eval loop, not with another full research detour

### Evidence
- Eval runs and lift outputs generated from the seeded batch
- UI + API wiring for `eval` and `audit` flows
- Local test coverage on the core run path

### Next (Day 07+)
- Iteration: batch decide, audit clarity, UI copy polish, and remaining quality work

---

## 27 August 2026 — Day 07 (batch ops + audit)

### Goal
Iteration: batch decision calls + a global audit trail with a clean demo path.

### What I built
- `POST /api/v1/cases/batch/decide` for multi-case rollout from the Home view
- `GET /api/v1/audit/recent` plus the audit list in the UI
- Home page copy and batch entry points aligned to the decision loop
- Case detail + audit trail remain scoped to the same workflow model

### Decisions
- Batch defaults to `auto_execute=true` to keep the demo fast and coherent
- Per-case detail remains available, while the global audit is optimized for discovery across many cases
- Day 07 is not a new architecture layer; it is iteration on the same loop

### Evidence
- `main.py` batch and audit routes
- `AuditPage.tsx` and `HomePage.tsx` wiring
- Local batch and audit flow validation

### Next (Day 08+)
- Baseline B visibility and policy comparison polish

---

## 28 August 2026 — Day 08 (Baseline B comparison)

### Goal
Make the evaluation story visibly compare three behaviors: Baseline A, Baseline B, and Rebound.

### What I built
- `EvalPage.tsx` comparison table across all three policies
- Clear labels for recovery rate, net value, cost, stop rate, and simulated share
- Honest simulated-output annotations preserved in the UI and summary text
- `rebound/eval/__init__.py` already exposes the Baseline B summary alongside Rebound

### Decisions
- Keep Baseline B visible as the alternate heuristic in the same run so judges can compare apples-to-apples
- Do not overstate the result as actual live revenue; the page explicitly states it is simulated
- The eval layer remains a decision aid, not a live payment system

### Evidence
- Eval comparison table output from `run_eval.py`
- UI policy-side-by-side view in `EvalPage.tsx`
- Local comparison pass across A / B / Rebound scenario outputs

### Next (Day 09+)
- Approval/escalate UX and edge-case hardening

---

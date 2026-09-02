# Build Schedule — 15 days (Aug 21 → Sep 4, 2026)

> Bias: **build → test → iterate → polish**.  
> Research foundation exists. After Aug 22, research only answers concrete implementation questions.

## Calendar

| Dates | Days | Focus | Output |
| --- | ---: | --- | --- |
| **Aug 21** | 1 | PS selection + research | Final PS + research notes |
| **Aug 22** | 1 | Problem decomposition + architecture | Architecture + MVP scope |
| **Aug 23–26** | **4** | Core development | **End-to-end MVP** |
| **Aug 27–28** | **2** | Iteration shipped | Batch/audit + Baseline B |
| **Aug 29–31** | **3** | Deferred milestones | Rolled into the Sep 1–2 completion sprint |
| **Sep 1** | **1** | Days 09–12 completion sprint | ✅ Gate clarity, regression + benchmark, and sensitivity in three focused commits |
| **Sep 2** | **1** | Days 13–15 completion sprint | ✅ Differentiation, demo runbook, submission package — **build complete** |
| **Sep 3** | **1** | Protected test + fix day | Full demo, regression, evidence capture, necessary fixes only |
| **Sep 4** | **1** | Final QA + submission | Submit the verified package |

## Ratio (approx.)

| Phase | Days |
| --- | ---: |
| Research / design | 2 |
| Building (MVP) | 4 |
| Shipped iteration (Aug 27–28) | 2 |
| Deferred capacity (Aug 29–31), recovered in sprint | 3 |
| Remaining-build completion sprint (Sep 1–2) | 2 |
| Dedicated validation | 1 |
| Submission | 1 |

---

## Testing is continuous — with a protected validation day on Sep 3

| Day | Build habit |
| --- | --- |
| Aug 23 | Build feature → test feature |
| Aug 24 | Build → test → find failure → fix |
| Aug 25 | Integrate → test integration → fix |
| Aug 26 | MVP → end-to-end test |
| Aug 27–28 | Every shipped change includes a check |
| Sep 1–2 | Run targeted checks with every remaining milestone push |
| Sep 3 | **Full-system validation** (baselines, edge cases, UI/API connection, demo rehearsal) — not first contact with testing |

---

## Four-day MVP sprint (Aug 23–26)

| Day | Focus | Done means |
| --- | --- | --- |
| **Aug 23 — Skeleton** | Backend + DB + APIs + frontend shell | Repo runs; empty paths wired |
| **Aug 24 — Core workflow** | Main user / merchant loop | Happy path without “smart” yet |
| **Aug 25 — Intelligence** | Models / agent / tooling / policy proposal | Decision path produces structured actions |
| **Aug 26 — Integration** | Connect rails → deployable MVP | **Ugly but working** end-to-end |

After Aug 26: remaining milestones are compacted into the Sep 1–2 completion sprint; Sep 3 is protected for verification and Sep 4 for submission.

---

## Hard rules

1. **Aug 21 ends research-as-selection.** Lock (or consciously defer lock with a buildable thesis) and stop browsing the domain for sport.
2. **Aug 22 is architecture + MVP scope only** — not another literature review.
3. **After Aug 22:** research only when it answers a concrete implementation question  
   (“A vs B for retries?” ✓ · “read everything about dunning?” ✗).
4. Do not spend days comparing LangGraph vs CrewAI vs “one more paper.” Prefer the simplest stack that ships the loop.
5. Continuous testing > big-bang testing.

---

## Completion sprint — build complete → submission

| When | Status / do |
| --- | --- |
| **Aug 21** | **DONE** — Track 03 locked as **Rebound** |
| **Aug 22** | **DONE** — Decomposition + architecture + MVP freeze |
| **Aug 23** | **DONE** — Skeleton API + DB + React shell |
| **Aug 24** | **DONE** — Core workflow decide → gate → execute → audit |
| **Aug 25** | **DONE** — EV / model intelligence (Day 05) |
| **Aug 26** | **DONE** — Eval lift + outcome audit (Day 06) |
| **Sep 1** | **DONE** — Days 09–12: gate clarity, regression + benchmark evidence, and sensitivity notes |
| **Sep 2** | **DONE** — Days 13–15: differentiation, demo polish, and submission package; build complete |
| **Sep 3** | **No planned feature work** — run the full demo, regression suite, connection checks, capture evidence, and fix only verified issues |
| **Sep 4** | Final checklist, video, public/package checks, then submit |

Architecture: [`architecture/README.md`](architecture/README.md) · MVP: [`architecture/mvp-scope.md`](architecture/mvp-scope.md) · Externals: [`docs/EXTERNAL_REQUIREMENTS.md`](docs/EXTERNAL_REQUIREMENTS.md)

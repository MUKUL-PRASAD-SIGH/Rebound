# Build Schedule — 15 days (Aug 21 → Sep 5, 2026)

> Bias: **build → test → iterate → polish**.  
> Research foundation exists. After Aug 22, research only answers concrete implementation questions.

## Calendar

| Dates | Days | Focus | Output |
| --- | ---: | --- | --- |
| **Aug 21** | 1 | PS selection + research | Final PS + research notes |
| **Aug 22** | 1 | Problem decomposition + architecture | Architecture + MVP scope |
| **Aug 23–26** | **4** | Core development | **End-to-end MVP** |
| **Aug 27–30** | **4** | Iteration + feature development | Strong V2/V3 |
| **Aug 31–Sep 1** | **2** | Serious evaluation | Benchmarks + edge cases |
| **Sep 2** | 1 | Differentiation | One/two standout features |
| **Sep 3** | 1 | Polish + deployment | Demo-ready product |
| **Sep 4** | 1 | Documentation + video | Submission package |
| **Sep 5** | 1 | Final QA + submission | Submit |

## Ratio (approx.)

| Phase | Days |
| --- | ---: |
| Research / design | 2 |
| Building (MVP) | 4 |
| Iteration | 4 |
| Evaluation (dedicated) | 2 |
| Differentiation + polish | 2 |
| Docs / video / submit | 2 |

---

## Testing is continuous — not only Aug 31–Sep 1

| Day | Build habit |
| --- | --- |
| Aug 23 | Build feature → test feature |
| Aug 24 | Build → test → find failure → fix |
| Aug 25 | Integrate → test integration → fix |
| Aug 26 | MVP → end-to-end test |
| Aug 27–30 | Every change ships with a check |
| Aug 31–Sep 1 | **Serious evaluation** (baselines, held-out batch, edge cases) — not first contact with testing |

---

## Four-day MVP sprint (Aug 23–26)

| Day | Focus | Done means |
| --- | --- | --- |
| **Aug 23 — Skeleton** | Backend + DB + APIs + frontend shell | Repo runs; empty paths wired |
| **Aug 24 — Core workflow** | Main user / merchant loop | Happy path without “smart” yet |
| **Aug 25 — Intelligence** | Models / agent / tooling / policy proposal | Decision path produces structured actions |
| **Aug 26 — Integration** | Connect rails → deployable MVP | **Ugly but working** end-to-end |

After Aug 26: **9 days left to make it excellent.**

---

## Hard rules

1. **Aug 21 ends research-as-selection.** Lock (or consciously defer lock with a buildable thesis) and stop browsing the domain for sport.
2. **Aug 22 is architecture + MVP scope only** — not another literature review.
3. **After Aug 22:** research only when it answers a concrete implementation question  
   (“A vs B for retries?” ✓ · “read everything about dunning?” ✗).
4. Do not spend days comparing LangGraph vs CrewAI vs “one more paper.” Prefer the simplest stack that ships the loop.
5. Continuous testing > big-bang testing.

---

## Today → tomorrow

| When | Status / do |
| --- | --- |
| **Aug 21** | **DONE** — Track 03 locked as **Rebound** |
| **Aug 22** | **DONE** — Decomposition + architecture + MVP freeze |
| **Aug 23** | **DONE** — Skeleton API + DB + React shell |
| **Aug 24** | **DONE** — Core workflow decide → gate → execute → audit |
| **Aug 25** | **DONE** — EV / model intelligence (Day 05) |
| **Aug 26+** | Eval lift → iteration → polish (local / next pushes) |

Architecture: [`architecture/README.md`](architecture/README.md) · MVP: [`architecture/mvp-scope.md`](architecture/mvp-scope.md) · Externals: [`docs/EXTERNAL_REQUIREMENTS.md`](docs/EXTERNAL_REQUIREMENTS.md)

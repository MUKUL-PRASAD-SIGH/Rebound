# Rebound — Razorpay AI Buildathon 2026

[![Track](https://img.shields.io/badge/Track-03%20AI%20Revenue%20Recovery-0A2540?style=for-the-badge)](https://razorpay.com/buildathon/)
  [![Status](https://img.shields.io/badge/Status-Build%20Complete-2E7D32?style=for-the-badge)](#project-status)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20·%20ML%20·%20React-136FEC?style=for-the-badge)](#planned-stack)
[![License](https://img.shields.io/badge/License-Private%20Lab-6B7280?style=for-the-badge)](#safety--secrets)

<p align="center">
  <strong>Expected-value decision layer for revenue recovery</strong><br/>
  Detect at-risk revenue → choose bounded interventions → execute via Razorpay-compatible workflows → measure incremental lift vs baseline
</p>

<p align="center">
  <a href="https://razorpay.com/buildathon/"><img src="https://img.shields.io/badge/Razorpay-AI%20Buildathon%202026-072654?logo=razorpay&logoColor=white" alt="Razorpay Buildathon" /></a>
  <img src="https://img.shields.io/badge/Build_complete-Sep%202%202026-success" alt="Build complete September 2" />
  <img src="https://img.shields.io/badge/MVP_target-26%20Aug%202026-blue" alt="MVP target" />
  <img src="https://img.shields.io/badge/Test-Sep%203%202026-blue" alt="Dedicated test date" />
  <img src="https://img.shields.io/badge/Submit-4%20Sep%202026-orange" alt="Submit date" />
  <img src="https://img.shields.io/badge/₹0-test--mode%20first-lightgrey" alt="Zero cost build" />
</p>

---

## What is Rebound?

**Rebound** is not “AI payment retries.”

Razorpay already provides subscription retries, payment-method update flows, Intelligent Retry themes, and Agent Studio recovery agents. Rebound sits **above** those rails as a **decision-intelligence layer**:

| Step | What happens |
| --- | --- |
| 1 | Detect revenue at risk (failed charges, degradation, abandonment signals) |
| 2 | Estimate recoverability and intervention expected value |
| 3 | Propose a structured action (retry signal, payment link, stop, escalate, …) |
| 4 | Enforce **deterministic guardrails** (allowlists, caps, stopping rules) |
| 5 | Execute only allowlisted Razorpay-compatible workflows (test-mode) |
| 6 | Report **incremental recovered value vs a fixed baseline** + full audit trail |

> **One-line differentiation:** Razorpay retries and Agent Studio run recovery playbooks; Rebound decides *whether / which / when* (including **stop**) and proves incremental lift.

Full lock write-up: [`research/12-final-selection.md`](research/12-final-selection.md) · Overview: [`docs/00-project-overview.md`](docs/00-project-overview.md)

---

## Project status

| Milestone | State | Date |
| --- | --- | --- |
| Repo lab notebook | ✅ Active | 21 Aug 2026 |
| All 5 tracks researched | ✅ Done | 21 Aug 2026 |
| Problem statement locked | ✅ **Track 03 / Rebound** | 21 Aug 2026 |
| Architecture + MVP scope | ✅ Done | 22 Aug 2026 |
| Skeleton (API + UI) | ✅ Done | 23 Aug 2026 |
| Core workflow (decide/execute/audit) | ✅ Done | 24 Aug 2026 |
| Intelligence (EV + model) | ✅ Done | 25 Aug 2026 |
| End-to-end MVP (eval lift) | ✅ Done | 26 Aug 2026 |
| Batch decide + global audit | ✅ Done | 27 Aug 2026 |
| Baseline B comparison | ✅ Done | 28 Aug 2026 |
| Completion sprint — Days 09–12 | ✅ Done | 1 Sep 2026 |
| Completion sprint — Days 13–15 | ✅ Build complete | 2 Sep 2026 |
| Dedicated test + bug-fix day | Scheduled | 3 Sep 2026 |
| Final QA + submission | Scheduled | 4 Sep 2026 |

Calendar: [`SCHEDULE.md`](SCHEDULE.md)

---

## Why this repo looks like a lab notebook

This is a **research-before-code** build. Day 01 exists so anyone reading the repo can see:

1. I read all five problem statements  
2. I researched what Razorpay already ships in 2026  
3. I rejected clone ideas (smart retries, chat-checkout demos, generic fraud)  
4. I locked a thesis with clear differentiation  

Start here for the journey:

| Doc | Purpose |
| --- | --- |
| [`research/13-how-i-chose-the-ps.md`](research/13-how-i-chose-the-ps.md) | How the PS was chosen |
| [`research/12-final-selection.md`](research/12-final-selection.md) | Locked decision |
| [`research/14-differentiation-vs-agent-studio.md`](research/14-differentiation-vs-agent-studio.md) | Anti-clone guardrail |
| [`architecture/README.md`](architecture/README.md) | Day 02 system design + MVP freeze |
| [`research/README.md`](research/README.md) | Full research index |
| [`BUILD_LOG.md`](BUILD_LOG.md) | Append-only daily diary |
| [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md) | How documentation is organized |

---

## Repo map

```text
razorpay-buildathon-2026/
├── README.md                 # You are here
├── SCHEDULE.md               # 15-day build-heavy calendar
├── BUILD_LOG.md              # Append-only chronological diary
├── .env.example              # Secrets template (never commit .env)
├── .gitignore
├── research/                 # Day 01 — PS research journey
├── docs/
│   ├── 00-project-overview.md
│   ├── 01-research.md … 07-final-results.md
│   ├── DOCUMENTATION_SYSTEM.md
│   ├── build-log/            # day-00.md, day-01.md, day-02.md, …
│   └── medium-drafts/        # Milestone articles (not daily posts)
├── evidence/                 # Screenshots, benchmarks, experiments
├── architecture/             # Day 02 — decomposition, MVP freeze, ADRs
└── src/                      # Day 03+ product code
```

**Status:** The project build is complete through Day 15. Sep 3 is reserved for end-to-end testing, evidence capture, and verified fixes only; submission is Sep 4. Externals: [`docs/EXTERNAL_REQUIREMENTS.md`](docs/EXTERNAL_REQUIREMENTS.md). Logs: [`docs/build-log/`](docs/build-log/README.md).

---

## 15-day plan (summary)

| Dates | Focus | Output |
| --- | --- | --- |
| Aug 21 | PS + research | ✅ Locked Rebound |
| Aug 22 | Decomposition + architecture | ✅ Architecture + MVP scope |
| Aug 23 | Skeleton | ✅ API + DB + React shell |
| Aug 24 | Core workflow | ✅ Decide → gate → execute → audit |
| Aug 25–26 | Intelligence → integrate | ✅ Day 05 EV + Day 06 eval lift |
| Aug 27 | Batch + audit | ✅ Day 07 batch decide + audit |
| Aug 28 | Baseline B | ✅ Day 08 policy comparison |
| Sep 1 | Days 09–12 | ✅ Gate clarity, regression + benchmarks, sensitivity |
| Sep 2 | Days 13–15 | ✅ Differentiation, demo runbook, submission package — build complete |
| Sep 3 | Dedicated validation | Full demo, regression, evidence capture, fixes only |
| Sep 4 | Final QA + submit | Submit the verified package |

**Rule after Aug 22:** research only for concrete implementation questions. Test continuously while building; Sep 3 is the protected full-system validation day, not first contact with testing.

---

## Planned stack

| Layer | Choice |
| --- | --- |
| API | FastAPI |
| ML | Rules + EV; sklearn/logistic (XGBoost optional) |
| Policy | Deterministic Python engine (mandatory) |
| UI | React + TypeScript |
| Data | SQLite + SQLAlchemy |
| Payments | Razorpay test-mode Payment Links |
| Frameworks | No LangGraph/CrewAI for MVP |

Details: [`architecture/`](architecture/README.md) · freeze: [`architecture/mvp-scope.md`](architecture/mvp-scope.md)

---

## Safety & secrets

- Never commit `.env`, API keys, webhook secrets, or personal data  
- Use [`.env.example`](.env.example) as the template  
- LLM is **never** unrestricted authority over money actions  
- Model **proposes** → policy engine **gates** → allowlisted execute → **audit**  
- Test-mode outcomes are labeled honestly — never pretend simulated ₹ are real
- Optional OpenAI proposals are schema-constrained, exclude customer identifiers, and fall back to the local EV proposer on any failure

---

## How to run

### One-time

```bash
python -m pip install -r requirements.txt
python src/scripts/generate_batch.py
python src/scripts/train_model.py
```

### API

```bash
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000
```

- Health: http://127.0.0.1:8000/api/v1/health  
- Seed: `POST /api/v1/ingest/synthetic` or `make seed`  
- Eval: `python src/scripts/run_eval.py`  
- Tests: `cd src && python -m pytest tests -q`

### Web

```bash
cd src/apps/web
npm install
npm run dev
```

Open http://127.0.0.1:5173 — Vite proxies `/api` to the backend. Demo steps: [`docs/submission/demo-runbook.md`](docs/submission/demo-runbook.md).

---

## Demo: what to show

For a strong 2–3 minute walkthrough, use this order:

1. **Overview** — frame the problem: recovery needs a decision controller, not more blind retries.
2. **Seed batch** — load the repeatable 60-case synthetic portfolio.
3. **Evaluation** — run it *before* batch execution and show Rebound beside Baseline A and Baseline B. Call the metric **simulated net-value delta**, never live revenue.
4. **One case** — preview the proposed action, expected value, confidence, and deterministic gate; then decide and execute it safely.
5. **Audit trail** — show the cross-case evidence that makes every decision traceable.

The recording-ready click path and spoken narration are in [`docs/submission/video-script.md`](docs/submission/video-script.md). Use the fuller local setup and rehearsal instructions in [`docs/submission/demo-runbook.md`](docs/submission/demo-runbook.md).

---

## How to follow along

```bash
git clone https://github.com/MUKUL-PRASAD-SIGH/razorpay-buildathon-2026.git
cd razorpay-buildathon-2026
```

1. Read [`docs/00-project-overview.md`](docs/00-project-overview.md)  
2. Skim [`research/12-final-selection.md`](research/12-final-selection.md)  
3. Follow [`BUILD_LOG.md`](BUILD_LOG.md) day by day  
4. Code appears under `src/` from Aug 23  

---

## Buildathon context

Student track for [Razorpay AI Buildathon](https://razorpay.com/buildathon/) — build something real, show the repo + pitch + architecture. Internship signal > vanity demos.

**Track 03 bar we are aiming at:** detect revenue at risk → choose intervention → execute bounded recovery → measure money recovered across a batch, with escalation, stopping rules, and an audit trail.

---

## Author

**Mukul Prasad** · CSE, M.S. Ramaiah Institute of Technology, Bengaluru  

Private lab → curated public artifact near submission.

---

<p align="center">
  <sub>Build complete · end-to-end validation 3 Sep · submit 4 Sep</sub>
</p>

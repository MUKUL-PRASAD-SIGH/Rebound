# Rebound — Razorpay AI Buildathon 2026

[![Track](https://img.shields.io/badge/Track-03%20AI%20Revenue%20Recovery-0A2540?style=for-the-badge)](https://razorpay.com/buildathon/)
[![Status](https://img.shields.io/badge/Status-Skeleton%20Running%20·%20MVP%20Build-1565C0?style=for-the-badge)](#project-status)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20·%20ML%20·%20React-136FEC?style=for-the-badge)](#planned-stack)
[![License](https://img.shields.io/badge/License-Private%20Lab-6B7280?style=for-the-badge)](#safety--secrets)

<p align="center">
  <strong>Expected-value decision layer for revenue recovery</strong><br/>
  Detect at-risk revenue → choose bounded interventions → execute via Razorpay-compatible workflows → measure incremental lift vs baseline
</p>

<p align="center">
  <a href="https://razorpay.com/buildathon/"><img src="https://img.shields.io/badge/Razorpay-AI%20Buildathon%202026-072654?logo=razorpay&logoColor=white" alt="Razorpay Buildathon" /></a>
  <img src="https://img.shields.io/badge/Day-03%20Complete-success" alt="Day 03 complete" />
  <img src="https://img.shields.io/badge/MVP_target-26%20Aug%202026-blue" alt="MVP target" />
  <img src="https://img.shields.io/badge/Submit-5%20Sep%202026-orange" alt="Submit date" />
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
| End-to-end MVP (ugly but working) | In progress | 23–26 Aug 2026 |
| Iteration V2/V3 | Planned | 27–30 Aug 2026 |
| Serious evaluation | Planned | 31 Aug–1 Sep 2026 |
| Differentiation + polish | Planned | 2–3 Sep 2026 |
| Docs, video, submit | Planned | 4–5 Sep 2026 |

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

**Next:** Aug 23 skeleton — see [`architecture/mvp-scope.md`](architecture/mvp-scope.md).

---

## 15-day plan (summary)

| Dates | Focus | Output |
| --- | --- | --- |
| Aug 21 | PS + research | ✅ Locked Rebound |
| Aug 22 | Decomposition + architecture | ✅ Architecture + MVP scope |
| Aug 23–26 | Core development | Skeleton ✅ · workflow → intelligence → integrate |
| Aug 27–30 | Iteration | Strong V2/V3 |
| Aug 31–Sep 1 | Evaluation | Benchmarks + edge cases |
| Sep 2–3 | Differentiation + polish | Demo-ready |
| Sep 4–5 | Docs + QA + submit | Submission package |

**Rule after Aug 22:** research only for concrete implementation questions. Test continuously while building — dedicated eval is Aug 31–Sep 1, not first contact with testing.

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

---

## How to run (Day 03 skeleton)

### API

```bash
python -m pip install -r requirements.txt
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000
```

- Health: http://127.0.0.1:8000/api/v1/health  
- Seed: `python src/scripts/seed_batch.py` (API must be up)  
- Or `POST http://127.0.0.1:8000/api/v1/ingest/synthetic`

### Web

```bash
cd src/apps/web
npm install
npm run dev
```

Open http://127.0.0.1:5173 — Vite proxies `/api` to the backend.

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
  <sub>Day 03 complete · Core workflow 24 Aug · MVP by 26 Aug · Submit by 5 Sep</sub>
</p>

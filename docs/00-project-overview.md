# 00 — Project Overview

> One-page truth. Locked 21 Aug 2026.

## Working title

**Rebound**

## One-liner

An expected-value decision layer that detects revenue at risk, chooses bounded recovery actions under policy limits, executes them through Razorpay-compatible workflows, and measures incremental recovered value vs a baseline.

## Track

**03 — AI Revenue Recovery** ([buildathon](https://razorpay.com/buildathon/))

## Problem

- **Who hurts?** Subscription / D2C merchants losing revenue to failed charges, stale methods, and weak recovery sequencing.
- **What is broken?** Retries and update links exist, but choosing *whether / which / when* to intervene (including stop) under cost and policy constraints is still under-specified — and easy to confuse with “smarter retries.”
- **Why Razorpay?** Rails + webhooks + test-mode + the real product baseline (Intelligent Retry, Agent Studio recovery) all live here.

## Solution (hypothesis)

Rebound: detect → score recoverability & intervention EV → agent proposes structured action → **deterministic guardrails** → allowlisted Razorpay action → outcome + audit → incremental lift vs fixed baseline.

## Target user

Merchant ops / revenue teams (demo persona: a test-mode merchant with a batch of at-risk subscriptions/checkouts).

## Scope for the buildathon

See [`SCHEDULE.md`](../SCHEDULE.md).

### In scope (MVP target by Aug 26)
- Ingest failure / at-risk events (synthetic + webhook-shaped)
- EV / policy decision engine with stopping rules
- Allowlisted actions (e.g. retry signal, payment-link recovery, stop/escalate)
- Ops UI: queue, decision explain, audit trail
- Batch evaluation: recovery rate + incremental value vs baseline

### Out of scope
- Recreating Razorpay core retries or cloning Agent Studio voice recovery
- Live WhatsApp/voice as a required dependency
- Open-ended research after Aug 22
- Framework tourism

## Success criteria

| Criterion | How we'll know |
| --- | --- |
| Demo works end-to-end | Ugly MVP by Aug 26; polished by Sep 3 |
| Clear Razorpay relevance | Test-mode / webhook-compatible loop |
| Measurable insight | Incremental recovered value vs baseline on held-out batch |
| Safety | No unrestricted LLM money actions; audit trail |
| Proof trail | Build log + commits + evidence |

## Stack (tentative — finalize Aug 22)

| Layer | Likely choice |
| --- | --- |
| API | FastAPI |
| ML | sklearn / XGBoost (+ simple baselines) |
| Agent/tools | Lightweight tool-calling; no framework maze |
| UI | React + TypeScript |
| Data | Postgres or SQLite for hackathon speed |
| Payments | Razorpay test-mode keys |

## Links

| Artifact | Link |
| --- | --- |
| Research lock | [`research/12-final-selection.md`](../research/12-final-selection.md) |
| How I chose | [`research/13-how-i-chose-the-ps.md`](../research/13-how-i-chose-the-ps.md) |
| Schedule | [`SCHEDULE.md`](../SCHEDULE.md) |
| Demo | TBD |
| Demo video | TBD |
| Medium journey | TBD |
| Public repo | Private until submission-ready |

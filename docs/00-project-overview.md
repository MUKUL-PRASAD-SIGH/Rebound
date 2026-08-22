# 00 — Project Overview

> One-page truth. PS locked 21 Aug 2026 · Architecture locked 22 Aug 2026.

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

Rebound: detect → score recoverability & intervention EV → propose structured action → **deterministic guardrails** → allowlisted Razorpay action → outcome + audit → incremental lift vs fixed baseline.

## Target user

Merchant ops / revenue teams (demo persona: a test-mode merchant with a batch of at-risk subscriptions/checkouts).

## Scope for the buildathon

See [`SCHEDULE.md`](../SCHEDULE.md) and frozen [`architecture/mvp-scope.md`](../architecture/mvp-scope.md).

### In scope (MVP by Aug 26)
- Synthetic batch ingest (≥50 cases) + webhook-shaped endpoint
- EV / policy decision engine with stopping rules
- Allowlisted actions: `silent_retry`, `payment_link`, `notify_update_method` (sim), `escalate`, `stop`
- Ops UI: queue, explain, audit, eval
- Batch evaluation: **lift_value** vs Baseline A

### Out of scope
- Live WhatsApp/voice; Agent Studio clones; replacing Razorpay retries
- Open-ended research; agent-framework tourism

## Success criteria

| Criterion | How we'll know |
| --- | --- |
| Demo works end-to-end | Ugly MVP by Aug 26; polished by Sep 3 |
| Clear Razorpay relevance | Test-mode Payment Link and/or documented dry-run |
| Measurable insight | `lift_value` on held-out/seed batch |
| Safety | Policy gate + audit; no unrestricted LLM money actions |
| Proof trail | Build log + commits + evidence |

## Stack (locked 22 Aug)

| Layer | Choice |
| --- | --- |
| API | FastAPI |
| ML / decide | Rules + EV; sklearn/logistic (or XGBoost if fits); optional LLM JSON proposer |
| Policy | Pure Python deterministic engine |
| UI | React + TypeScript |
| Data | SQLite + SQLAlchemy |
| Payments | Razorpay test-mode (Payment Links primary) |
| Agent frameworks | **None** for MVP |

Architecture: [`architecture/README.md`](../architecture/README.md)

## Links

| Artifact | Link |
| --- | --- |
| Research lock | [`research/12-final-selection.md`](../research/12-final-selection.md) |
| How I chose | [`research/13-how-i-chose-the-ps.md`](../research/13-how-i-chose-the-ps.md) |
| Architecture | [`architecture/README.md`](../architecture/README.md) |
| MVP scope | [`architecture/mvp-scope.md`](../architecture/mvp-scope.md) |
| Schedule | [`SCHEDULE.md`](../SCHEDULE.md) |
| Demo | TBD |
| Demo video | TBD |
| Public repo | https://github.com/MUKUL-PRASAD-SIGH/razorpay-buildathon-2026 |

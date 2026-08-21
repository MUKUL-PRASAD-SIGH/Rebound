# 05 — Track 04: AI Finance Controller

> Status: researched (first pass) · Clear rubric · Differentiation risk · Not selected yet

## What the track asks

Close **one** finance-ops loop across a **50+ record** batch of synthetic data.

Report:

- match rate
- exceptions that could not be resolved

Example directions: multi-source reconciliation, settlement Q&A, forward cash forecaster, tax-line matcher.

Why-now on the page: verification capacity (not generation speed) is the bottleneck; reconciliation / settlement / forecasting still manual.

## What I thought at first

"Reconciliation + LLM = safe hackathon project with a clean scoreboard."

Then: is there enough AI depth, or is this a dashboard with a chatbot stuck on top?

## What Razorpay already provides

| Capability | Notes | Source |
| --- | --- | --- |
| Settlement reports / dashboard reconciliation workflows | Merchants already reconcile settlements vs bank credits using Razorpay reports (standard PG ops) | Docs / dashboard practice; **TODO:** cite exact settlement docs pages used in build |
| **RazorpayX ↔ Tally** | Two-way integration for vendor payments, bookkeeping, reconciliation flows | [RazorpayX-Tally](https://razorpay.com/docs/x/vendor-payments/tally/) |
| **RazorpayX Accounting** | Sync account statements / payouts / vendor payments with Zoho Books or Tally | [Accounting integrations](https://razorpay.com/docs/x/accounting/) |
| **Agent Studio / Agentic Business Banking agents** | Bookkeeping agent, reporting agent, cashflow / insights agents appear in Sprint / Agent Studio narratives | [Sprint 2026](https://razorpay.com/sprint/26) · [Agent Studio newsroom](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/) |
| **Smart Collect / collections automation** | Banking-side collections + reconciliation themes | Sprint 2026 Business Banking section |

### Realization

Razorpay is already pushing automated bookkeeping and agentic finance ops. A student "recon bot" that fuzzy-matches 50 CSV rows can meet the literal bar and still feel shallow to an engineer.

## Where AI depth can still exist

Interesting technical split:

1. **Deterministic matching first** (IDs, amounts, dates, fees, tax lines)
2. **LLM / ML only on residual exceptions** (ambiguous narrations, partial refunds, fee splits)
3. **Human-in-the-loop** for high-impact exceptions
4. Metrics: match rate, exception rate, time-to-close, **hallucinated match rate** (critical)

The project becomes impressive only if I show:

- a hard baseline (rules only)
- lift from AI on *exceptions*, not on trivial exact matches
- an honest list of cases the system refuses to auto-post

## Hiring / judging signal

Pros:

- Clear evaluation (50+ batch, match rate, exceptions)
- Production-oriented discipline (audit, refusal, HITL)

Cons:

- Easy to look like a polished internal tool without Razorpay-specific insight
- Overlap with Bookkeeping / Reporting agents in Razorpay's own agentic banking story
- Less "agentic payments era" narrative than Tracks 01/03

## Fit with my skills

Good: data pipelines, evaluation harnesses, RAG over policies, FastAPI.  
Weaker motivational fit vs my preference for decision systems under uncertainty.

## Current verdict on Track 04

**Viable backup**, especially if Track 03 collapses under API/product overlap.

Not my first choice unless I can design an exception-first reconciler that would still impress a Razorpay finance-platform engineer.

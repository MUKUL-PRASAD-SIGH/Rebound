# 03 — Track 02: AI Risk Manager

> Status: researched (first pass) · High skill fit · High overlap + data risk · Not selected yet

## What the track asks

Build a working **detector, verifier, or auto-responder** for one class of loss, with **measured precision and recall on a held-out test set**.

Example directions: chargeback evidence responder, return-risk scorer, fraud-spike detector, abuse-ring sentinel.

Hard rules from the page:

- Honest metrics including **false-positive cost**
- **Strictly defense-only** (offense-capable work is disqualified)

## What I thought at first

"I know tabular ML and anomaly detection. Fraud classifier = strong technical show."

Then I asked the awkward question: what data do I actually have?

## What Razorpay already provides / is building

| Capability | Notes | Source | Overlap |
| --- | --- | --- | --- |
| **Vulcan** | Network-level fraud patterns across merchants; ~3k signals/txn claimed; company-reported lifts | [Vulcan blog](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/) · coverage e.g. Fortune India (18 Aug 2026) | Competing with foundation-model fraud intelligence is a losing student strategy |
| **Razorpay SHIELD** | Payments risk suite: AI-ML risk engine, chargeback protection, risk dashboard (esp. international) | [SHIELD blog](https://razorpay.com/blog/razorpay-upticks-success-rates-razorpay-shield/) | Chargeback / risk product surface already exists |
| **Thirdwatch** | Fraud prevention suite: monitoring, customizable risk scoring, alerts | [Payment gateways reduce fraud risk blog](https://razorpay.com/blog/payment-gateways-reduce-fraud-risk/) | Generic "fraud detector" recreates a marketed suite |
| **Bumblebee** | Multi-agent merchant review system; engineering post describes architecture & ops impact | [Engineering: Meet Bumblebee](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51) (published ~Aug 2026) | Multi-agent fraud review is an internal Razorpay story judges already know |
| **Agent Studio — Dispute Auto-Responder / Dispute Expert** | Chargeback evidence gathering, win-probability, submit or draft-for-approval | [Sprint 2026](https://razorpay.com/sprint/26) · [Agent Studio principles](https://razorpay.com/blog/razorpay-agent-studio-principles-guardrails-and-merchant-control/) · [Newsroom FTX’26](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/) | Chargeback auto-responder example direction has direct product overlap |

### Realization

Track 02 is not "is fraud important?" — of course it is.

The question is: **can a student team produce a defensible risk system with honest precision/recall without proprietary network data?**

Without Razorpay-scale graph features, most public datasets turn into generic Kaggle classifiers. That is weak hiring signal even if the ROC curve looks pretty.

## Where there might still be an edge

Possible narrower bets (hypotheses):

1. **Return / RTO risk scorer for D2C** using merchant-ownable features (address quality, SKU history, COD patterns) — Sprint also lists RTO-related agents, so differentiate carefully.
2. **Chargeback evidence packager** that is explicitly *human-in-the-loop* and focuses on retrieval + structured evidence quality metrics — but Agent Studio already markets this.
3. **Abuse-ring sentinel on synthetic graph data** with clear evaluation protocol — technically interesting; demo realism is harder.

## Evaluation honesty test

If I pick this track I must ship:

- Held-out test set
- Precision, recall, F1, and ideally PR-AUC
- **False-positive cost model** (blocked good customer ≈ lost GMV / support load)
- Explicit statement of what the model cannot see (no network-level features)

If I cannot get a credible dataset story in week 1, this track collapses into theater.

## Flashy vs real

| Idea | Risk |
| --- | --- |
| Generic fraud classifier on public card data | Looks ML-y; weak Razorpay relevance; low differentiation |
| "Graph neural network abuse rings" without real graph | Easy to overclaim |
| Dispute responder clone of Agent Studio | High overlap |
| Narrow RTO/return model with cost-sensitive thresholding | More honest if data is synthetic-but-principled |

## Fit with my skills

Strongest track for pure ML craft (XGBoost, cost-sensitive learning, calibration).  
Weakest track for **data realism** and **avoiding product overlap**.

## Current verdict on Track 02

**Do not default here just because I like ML.**

Only keep if I find a **narrow loss class** with:

- a dataset I can defend,
- metrics that include FP cost,
- and a gap that is clearly *not* Vulcan/SHIELD/Bumblebee/Dispute Agent.

Right now that bar is not cleared. Parked unless a crisp niche appears.

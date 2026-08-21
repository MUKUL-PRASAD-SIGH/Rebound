# 04 — Track 03: AI Revenue Recovery

> Status: researched · **Selected as Rebound (locked 21 Aug 2026)** · See [`12-final-selection.md`](./12-final-selection.md)

## What the track asks

Build an agent that:

1. detects revenue at risk,
2. determines the right intervention,
3. executes a **bounded** recovery workflow.

Scope on the page includes payment failures, checkout abandonment, overdue receivables — not only subscriptions.

The bar: measured money recovered across a batch; compliant escalation; **stopping rules**; audit trail.

Example directions: payment degradation → root cause → recovery; checkout drop-off; failed-subscription recovery; B2B receivables; mandate retry sequencer; Hinglish voice recovery; promise-to-pay tracker.

## First instinct (and why it was wrong)

My first instinct was almost automatic:

> "Build an AI payment-retry agent."

It sounded perfect for Track 03. It also sounded too obvious.

So I checked what Razorpay already ships.

That changed the question.

## What Razorpay already provides (retries are not empty space)

### 1) Subscription payment retries (docs)

Official docs: [Payment Retries](https://razorpay.com/docs/payments/subscriptions/payment-retries/?preferred-country=IN)

Verified behavior (docs, not marketing spin):

- Failed auto-charge → subscription `pending`
- Webhooks: `subscription.pending`, `subscription.halted`
- Automatic retries (method-specific models; cards often next-day / multi-day windows depending on region/docs section)
- Customer email with link to update payment method
- Hosted page to retry / change card / switch method
- Manual charge of `issued` invoices in some cases
- After retries exhausted → `halted`

**Conclusion:** "We added retries" is not a project. The rail exists.

### 2) Smart Retry language in Razorpay content

Razorpay's own subscriptions marketing/docs mention smart/automatic retry behavior aimed at involuntary churn ([Subscriptions overview](https://razorpay.com/docs/payments/subscriptions/?preferred-country=IN), [churn guide](https://razorpay.com/blog/reduce-churn-recurring-payments-guide/)).

I treat blog "smart retry" claims carefully and prefer docs for mechanics. Either way: retry timing is not an untouched wilderness.

### 3) Intelligent Retry Engine / Intelligent Revenue-Protect (FTX 2026)

From [UPI Autopay with Intelligent Revenue-Protect](https://razorpay.com/blog/upi-autopay-with-intelligent-revenue-protect/):

- Intelligent Retry Engine (beta at FTX 2026): merchant-configurable retry strategies / templates
- WhatsApp recovery links / reminders for failed debits
- Broader "Revenue-Protect" framing for Autopay lifecycle

From [Sprint 2026](https://razorpay.com/sprint/26): Intelligent Retry Engine listed under Payment Gateway updates.

**Implication:** even "smarter retry schedules" is moving into Razorpay product surface.

### 4) Agent Studio — Subscription Recovery + Abandoned Cart agents

From Razorpay newsroom / blogs:

- [Agent Studio launch (FTX’26)](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/)
- [Agent Studio principles & guardrails](https://razorpay.com/blog/razorpay-agent-studio-principles-guardrails-and-merchant-control/)
- [agent-studio product page](https://razorpay.com/agent-studio/)

Notable agents:

- **Subscription Recovery Agent** — failed subscriptions, smarter retry logic, targeted nudges; voice-led variants mentioned with partners (e.g. ElevenLabs in newsroom)
- **Abandoned Cart Conversion Agent** — voice-led cart recovery with payment link

**Implication:** "voice calls customers about failed payments" is also not an empty demo niche.

## So is Track 03 dead?

No — but the **naive version** is dead.

What still looks open (hypothesis):

> Can AI decide which revenue is actually recoverable, which intervention is economically optimal, when to act, when **not** to act, and when to escalate — on top of Razorpay's existing retry / link / webhook infrastructure?

That is a **decision-intelligence / orchestration** layer, not a retry reinvent.

## The more interesting problem

When a payment fails or a checkout dies, the merchant faces a menu:

| Intervention family | Examples | Costs / risks |
| --- | --- | --- |
| Silent retry | Re-charge via existing subscription/invoice APIs | Irritation, issuer retry limits, duplicate charges if careless |
| Method update | Hosted update link / payment method change | Customer effort |
| Soft outreach | Email / WhatsApp / in-app | Channel fatigue, compliance |
| Hard outreach | Voice call | High cost, brand risk |
| Commercial concession | Discount / pause / plan change | Margin destruction |
| Escalate / stop | Human review or cease contact | Opportunity cost of stopping too early |

The non-trivial ML/decision problem:

\[
\mathbb{E}[\text{recovered}] = P(\text{recover} \mid \text{intervention}, x) \cdot \text{value}(x) - \text{cost}(\text{intervention}, x)
\]

Plus constraints:

- retry limits
- communication limits
- discount caps
- confidence thresholds
- stopping rules
- approval gates for high-value or high-risk actions

### What AI contributes that if-else dunning may not

- Estimate recovery probability by failure reason + customer context
- Estimate response probability by channel
- Choose intervention under cost and policy constraints
- Decide **not** to spend recovery effort on low-EV cases
- Explain the choice for audit

Deterministic software can encode policies.  
Learning systems earn their keep when the mapping from context → optimal bounded action is high-dimensional and measurable.

## Architecture sketch (production-oriented, not "production")

```text
signals (webhooks / synthetic events)
        ↓
feature + diagnosis layer
        ↓
models: P(recover), P(respond), value, cost
        ↓
agent proposes structured action
        ↓
deterministic policy / guardrail engine
  (allowlist, limits, stopping rules, confidence)
        ↓
approval gate (if needed)
        ↓
Razorpay-compatible execution
  (test-mode charge / payment link / invoice / noted outreach)
        ↓
outcome + incremental metric vs baseline
        ↓
audit trail
```

Why this is safer than "LLM calls charge API":

- model proposes; policy decides
- money actions are allowlisted
- duplicates / timeouts / malformed JSON are handled outside the LLM
- every action is explainable after the fact

## Existing solutions outside Razorpay (adjacent)

Globally, subscription recovery is a mature category:

- Stripe Billing: Smart Retries + revenue recovery tooling ([Stripe docs](https://docs.stripe.com/billing/revenue-recovery))
- Third parties (e.g. Churnkey-style dunning + payment walls) sit *above* processor retries

**Insight:** the industry pattern is layers:

1. processor retries
2. customer communication / payment update UX
3. decisioning / experimentation / incremental lift

Razorpay is pushing (1) and parts of (2)/(3) via Intelligent Retry + Agent Studio.  
A student project only makes sense if it is clearly a **measurable decision layer** with honest baseline comparison — not a clone of Subscription Recovery Agent aesthetics.

## Flashy vs real for Track 03

| Idea | Verdict |
| --- | --- |
| AI retries failed cards | Reject — overlaps docs + Intelligent Retry |
| Voice dunning clone | Reject unless radically different metric/policy story — Agent Studio overlap |
| Checkout abandonment WhatsApp blaster | Weak — easy spam; hard to prove incremental lift |
| **EV-aware recovery controller** with baselines, stopping rules, audit | Keep — aligns with track bar; harder; more engineer-shaped |
| B2B receivables chaser on invoices | Possible variant if invoice APIs + synthetic AR are clean in test-mode |

## Fit with my skills

Excellent match: tabular ML (XGBoost), expected-value framing, FastAPI orchestration, agent proposal + tool calling, React ops console, evaluation harness.

## ₹0 feasibility

| Piece | Plan |
| --- | --- |
| Payments | Razorpay test-mode subscriptions / invoices / payment links |
| Failures | Synthetic failure reasons + webhook fixtures (clearly labeled simulated) |
| Outreach | Log/simulate channels; optional free email sandbox; do not fake WhatsApp delivery metrics |
| Models | sklearn / XGBoost / local or free LLM tier for diagnosis text only |
| Metric | Incremental recovered revenue vs fixed-policy baseline on a held-out batch |

Never pretend a test-mode charge is a real rupee. Report **simulated recovered value** honestly if live merchant money is unavailable.

## Current verdict on Track 03

**Leading candidate — conditional.**

Condition: the thesis must be decision intelligence above existing Razorpay recovery rails, with:

- baselines,
- EV / policy constraints,
- stopping rules,
- audit trail,
- measured batch recovery.

If I catch myself sliding back into "smart retry demo," reject my own idea again.

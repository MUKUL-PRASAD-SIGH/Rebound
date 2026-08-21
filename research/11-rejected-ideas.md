# 11 — Ideas I Rejected

> This file is the anti-hindsight log. Attractive ideas that research killed (or wounded).

## Rejected 1 — "AI payment retry agent"

**What I initially considered:** An agent that watches failed subscription charges and retries smarter.

**Why it sounded attractive:** Perfect Track 03 slogan. Easy demo. Obvious merchant value.

**What research revealed:**

- Razorpay Subscriptions already auto-retry and notify; hosted update flows exist ([Payment Retries docs](https://razorpay.com/docs/payments/subscriptions/payment-retries/?preferred-country=IN))
- Intelligent Retry Engine / Revenue-Protect expands configurable retries + recovery messaging ([blog](https://razorpay.com/blog/upi-autopay-with-intelligent-revenue-protect/))
- Agent Studio Subscription Recovery Agent targets this job ([newsroom](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/))

**Overlap:** Core retry rail + official recovery agent.

**Why rejected (as the final idea):** Rebuilding retries is not a gap; it is a recreation.

**Insight gained:** Track 03 value, if any, is **which intervention / when / whether** — not **how to retry**.

---

## Rejected 2 — "ChatGPT checkout that pays with UPI"

**What I initially considered:** Conversational shopping demo ending in Razorpay payment.

**Why attractive:** Agentic commerce zeitgeist; great video.

**What research revealed:**

- Razorpay Agentic Payments already pursues in-chat / in-app / voice commerce ([product](https://razorpay.com/agentic-payments/))
- Claude / ChatGPT pilots with major consumer brands exist
- UPI Reserve Pay is the consent primitive for agent debit

**Why rejected:** Demo-theater against Razorpay's own narrative unless the novelty is merchant readiness / catalog / policy — not the payment moment itself.

**Insight gained:** Do not compete with the keynote. Compete with the unglamorous merchant gap behind it.

---

## Rejected 3 — "Generic fraud classifier"

**What I initially considered:** XGBoost/PyTorch fraud model with nice PR curve.

**Why attractive:** Matches my ML strengths; Track 02 bar asks for precision/recall.

**What research revealed:**

- Vulcan claims network-level fraud intelligence
- SHIELD / Thirdwatch already productize risk
- Without proprietary graph/network features, public datasets skew generic

**Why rejected (for now):** High chance of "Kaggle with a Razorpay theme."

**Insight gained:** Defense ML needs a narrow loss class + cost-sensitive honesty + data I can defend.

---

## Rejected 4 — "Chargeback auto-responder"

**What I initially considered:** Agent gathers evidence and answers chargebacks.

**Why attractive:** Listed almost literally in Track 02 examples; agentic; hiring-relevant.

**What research revealed:** Agent Studio Dispute Auto-Responder / Dispute Expert is explicitly marketed.

**Why rejected:** Direct SKU collision.

**Insight gained:** Example directions on the buildathon page are prompts, not empty land.

---

## Rejected 5 — "Finance chatbot that answers settlement questions"

**What I initially considered:** RAG over settlement CSVs + natural language Q&A.

**Why attractive:** Fast to build; Track 04 adjacent.

**Why rejected:** Thin AI; weak measurable ops outcome unless paired with exception-closing actions and accuracy on a batch.

**Insight gained:** Track 04 rewards closed loops, not chat.

---

## Wounded but not fully dead

### A) Voice recovery in Hinglish
Wounded by Agent Studio voice recovery narratives. Could revive only with a clearly different decision core + metrics (not voice novelty).

### B) Checkout abandonment recovery
Wounded by Abandoned Cart agent. Revive only as part of a multi-intervention EV controller with baseline lift.

### C) Agent-readable catalog
Still alive as a Track 01 candidate, pending protocol/API feasibility research.

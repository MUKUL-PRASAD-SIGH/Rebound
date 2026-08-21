# 09 — Existing Solutions

> Goal: avoid inventing products that already exist.  
> Split: Razorpay-native vs adjacent market.

## Razorpay-native (directly relevant)

### Payment success & intelligence

- Routing / optimiser-style success improvement (historical product + Vulcan routing story)
- Checkout personalization / offer targeting (Vulcan blog)

### Fraud & risk

- SHIELD
- Thirdwatch
- Internal systems like Bumblebee
- Vulcan network fraud signals

### Recurring + recovery

- Subscriptions lifecycle (`pending` / `halted`, webhooks)
- Automatic payment retries + hosted payment-method update
- Intelligent Retry Engine (beta framing)
- WhatsApp recovery link patterns in Revenue-Protect messaging
- Agent Studio: Subscription Recovery, Abandoned Cart

### Agentic commerce

- Agentic Payments (in-app, LLM, voice)
- UPI Reserve Pay
- Brand pilots (Zomato/Swiggy/Zepto/others depending on announcement)

### Finance ops

- Settlements + reports
- RazorpayX accounting integrations (Tally, Zoho Books)
- Bookkeeping / reporting / receivables agent directions

## Adjacent market (not Razorpay, but shape the category)

| Category | Examples (illustrative) | Lesson |
| --- | --- | --- |
| Processor smart retries | Stripe Smart Retries | Timing optimization is table stakes at mature processors |
| Dunning / involuntary churn platforms | Churnkey-class tools | Value often sits in multi-channel recovery + payment update UX + measurement above the processor |
| Fraud platforms | Sift / Riskified / etc. (general market) | Network effects + labels dominate; student clones struggle |
| Agentic commerce protocols | ACP / AP2 / x402 / UAP (named on buildathon page) | **TODO:** verify each protocol's maturity before depending on it |

## Gap lens (how I use this file)

An idea is interesting only if it targets one of:

1. **Composition gap** — stitching existing Razorpay rails into a better decision loop
2. **Measurement gap** — incremental lift vs baseline that merchants cannot see today
3. **Policy / safety gap** — bounded autonomy, stopping rules, auditability
4. **Merchant readiness gap** — making a business operable by AI buyers/agents
5. **Exception intelligence gap** — AI on residuals after deterministic systems

If the idea is "rebuild X that Razorpay already lists on Sprint," it fails this file.

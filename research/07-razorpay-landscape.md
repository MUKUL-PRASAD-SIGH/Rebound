# 07 — Razorpay Landscape (what exists vs what builders are asked to explore)

> First pass: 21 Aug 2026. Fact vs hypothesis labeled.

## Snapshot

Razorpay in 2026 is not "a payment gateway plus a hackathon."

From primary pages and newsroom posts, the company is publicly positioning around an **agentic stack**: agentic payments, agentic platform, Agent Studio, MCP for builders, plus deeper AI in routing/fraud/checkout (Vulcan).

That landscape is the board I am playing on.

## Layer cake (my map)

```text
┌──────────────────────────────────────────────┐
│ Merchant / developer agents (Agent Studio,   │
│ MCP tools, dashboard copilots, custom agents)│
├──────────────────────────────────────────────┤
│ Agentic commerce experiences                 │
│ (in-app chat, LLM chat, voice)               │
├──────────────────────────────────────────────┤
│ Consent & execution rails                    │
│ (UPI Reserve Pay, mandates, Autopay, links)  │
├──────────────────────────────────────────────┤
│ Core payment intelligence                    │
│ (routing, fraud, checkout personalization —  │
│  Vulcan + prior ML systems)                  │
├──────────────────────────────────────────────┤
│ Payments + banking APIs / webhooks / reports │
└──────────────────────────────────────────────┘
```

Hackathon leverage is usually **above** core intelligence and **beside** official agents — composing rails, not reimplementing them.

## Product inventory relevant to tracks

### Payments intelligence

| Item | Relevance | Notes |
| --- | --- | --- |
| Vulcan | Tracks 01, 02, 03 | Foundation model for payments patterns; routing/fraud/checkout |
| Optimiser / smart routing (historical + Sprint updates) | 01, 03 | Success-rate optimization is core PG work |

### Risk

| Item | Relevance | Notes |
| --- | --- | --- |
| SHIELD | 02 | Risk suite / chargeback protection |
| Thirdwatch | 02 | Fraud monitoring suite |
| Bumblebee | 02 | Internal multi-agent merchant review |

### Recurring revenue & recovery

| Item | Relevance | Notes |
| --- | --- | --- |
| Subscriptions + Payment Retries | 03 | Documented pending/halted/retry/hosted update |
| Intelligent Retry Engine | 03 | Merchant-configurable retries; WhatsApp recovery themes |
| Agent Studio Subscription Recovery | 03 | Official recovery agent |
| Agent Studio Abandoned Cart agent | 03 / 01 | Checkout recovery productized |

### Agentic commerce

| Item | Relevance | Notes |
| --- | --- | --- |
| Agentic Payments suite | 01 | In-app / LLM / voice |
| UPI Reserve Pay | 01 | Bounded consent for agent spend |
| Claude / ChatGPT pilots | 01 | Brand pilots; not fully open playground |
| Razorpay MCP | 01–05 | Builder interface to APIs |

### Finance ops

| Item | Relevance | Notes |
| --- | --- | --- |
| RazorpayX Tally / Zoho | 04 | Accounting sync & reconciliation automation |
| Bookkeeping / Reporting / Receivables agents | 04 / 03 | Agentic banking direction |

## Distinctions I will keep repeating

| Bucket | Meaning |
| --- | --- |
| **Already does** | Documented product behavior merchants can use today |
| **Actively building** | Announced / beta / pilot / Sprint launch |
| **Hackathon asks** | Builder exploration space with evaluation bars |
| **Merchant still needs** | Gaps above or around the stack (hypothesis until validated) |
| **Our project could add** | Only after the four above are checked |

## Working rule for idea quality

If my one-sentence pitch still works after deleting the words "AI" and "agent," it might be fine software — but I must still explain what learning/decisioning uniquely contributes.

If my one-sentence pitch stops working after I subtract Razorpay's existing retry/agent/fraud products, the idea was a clone.

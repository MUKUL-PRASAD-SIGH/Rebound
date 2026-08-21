# Sources

> Primary over secondary. Dated when known.  
> If I could not verify something, it is marked unverified / TODO — not filled with guesses.

## Official buildathon

| Date accessed | Source | Use |
| --- | --- | --- |
| 2026-08-21 | [Razorpay AI Buildathon](https://razorpay.com/buildathon/) | Track definitions, bars, internship offer |

## Razorpay — AI / agentic / foundation

| Date | Source | Use |
| --- | --- | --- |
| 2026-08 (announced ~18 Aug per coverage) | [One Foundation Model… (Vulcan)](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/) | Vulcan scope: routing, fraud, checkout |
| 2026-08-18 | [AWS press — Vulcan](https://press.aboutamazon.com/aws-international/2026/8/razorpay-launches-vulcan-indias-first-ai-payments-foundation-model-fueled-by-nvidia-and-aws-re-architecting-payments-for-a-350-bn-e-comm-future-by-2030) | Independent-ish confirmation of launch framing |
| 2026-08-18 | [Fortune India — Vulcan](https://www.fortuneindia.com/technology/razorpay-launches-vulcan-ai-model-with-nvidia-aws-to-boost-payment-success-fraud-detection/154423) | Company-reported metrics (treat as claims) |
| 2026-02-20 | [Agentic Payments & NPCI (Claude)](https://razorpay.com/blog/agentic-payments-and-npci/) | Claude pilot; Reserve Pay consent model |
| 2026-02-20 | [Newsroom — Claude agentic payments](https://razorpay.com/newsroom/razorpay-npci-launch-agentic-payments-on-claude-powering-zomato-swiggy-zepto-at-the-india-ai-impact-summit/) | Brand pilots; pilot-phase language |
| — | [UPI Reserve Pay](https://razorpay.com/blog/upi-reserve-pay/) | SBMD / bounded agent debit; ChatGPT/Gemini/Claude mentions |
| — | [Agentic Payments product](https://razorpay.com/agentic-payments/) | In-app / LLM / voice suite; Reserve Pay Live; Circle Coming soon |
| — | [ChatGPT agentic payments blog](https://razorpay.com/blog/razorpay-unveils-agentic-payments-on-chatgpt-with-npci-indias-first-ai-powered-conversational-payment-experience/) | Earlier ChatGPT private beta narrative |
| 2026-04-06 | [Codex + Razorpay newsroom](https://razorpay.com/newsroom/razorpay-launches-upi-and-all-payment-methods-within-openais-codex-enabling-developers-to-build-and-monetise-apps-instantly/) | MCP / builder monetization |
| — | [Sprint 2026](https://razorpay.com/sprint/26) | Agentic stack catalog; Intelligent Retry; agents list |

## Razorpay — Agent Studio

| Date | Source | Use |
| --- | --- | --- |
| FTX’26 | [Newsroom — Agent Studio](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/) | Launch agents incl. subscription recovery, disputes, cart |
| — | [Agent Studio principles & guardrails](https://razorpay.com/blog/razorpay-agent-studio-principles-guardrails-and-merchant-control/) | Merchant control; recovery/dispute agent behavior |
| — | [Agent Studio blog](https://razorpay.com/blog/agent-studio-ai-agents-by-razorpay/) | Product framing |
| — | [Agent Studio](https://razorpay.com/agent-studio/) | Product page |

## Razorpay — subscriptions / recovery docs

| Date accessed | Source | Use |
| --- | --- | --- |
| 2026-08-21 | [Payment Retries docs](https://razorpay.com/docs/payments/subscriptions/payment-retries/?preferred-country=IN) | pending/halted, retries, hosted update |
| 2026-08-21 | [Subscriptions overview](https://razorpay.com/docs/payments/subscriptions/?preferred-country=IN) | Smart payment retries mention |
| 2026-08-21 | [Subscription states](https://razorpay.com/docs/payments/subscriptions/states/) | State machine details |
| — | [Reduce churn guide](https://razorpay.com/blog/reduce-churn-recurring-payments-guide/) | Marketing-level smart retry / dunning discussion (verify vs docs) |
| — | [Intelligent Revenue-Protect / Autopay](https://razorpay.com/blog/upi-autopay-with-intelligent-revenue-protect/) | Intelligent Retry Engine |

## Razorpay — risk / fraud

| Source | Use |
| --- | --- |
| [SHIELD blog](https://razorpay.com/blog/razorpay-upticks-success-rates-razorpay-shield/) | Risk suite / chargeback protection |
| [Payment gateways reduce fraud risk](https://razorpay.com/blog/payment-gateways-reduce-fraud-risk/) | Thirdwatch framing |
| [Bumblebee engineering post](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51) | Multi-agent merchant review |

## Razorpay — finance / accounting

| Source | Use |
| --- | --- |
| [RazorpayX-Tally](https://razorpay.com/docs/x/vendor-payments/tally/) | Reconciliation / bookkeeping automation |
| [Accounting integrations](https://razorpay.com/docs/x/accounting/) | Zoho Books / Tally sync |

## Builder tooling

| Source | Use |
| --- | --- |
| [razorpay/razorpay-mcp-server](https://github.com/razorpay/razorpay-mcp-server) | Official MCP tools |

## Adjacent industry (non-Razorpay)

| Source | Use |
| --- | --- |
| [Stripe Revenue Recovery](https://docs.stripe.com/billing/revenue-recovery) | Processor-level recovery layering pattern |
| [Stripe Smart Retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries) | Retry timing as table stakes |
| Churnkey guides/blogs | Example of above-processor dunning category (secondary; metrics are vendor-claimed) |

## Unverified / TODO before public claims

- [ ] Primary NPCI documentation for UAP / Reserve Pay regulatory framing
- [ ] Primary specs for ACP, AP2, x402 (buildathon mentions)
- [ ] Exact Razorpay test-mode coverage checklist with a sandbox key
- [ ] Whether Agent Studio agents are available to student accounts or only marketing/early access
- [ ] Third-party audits of Vulcan metrics (none found in first pass; treat metrics as company-reported)

## Integrity rules for this folder

1. Prefer razorpay.com docs/newsroom/blog for Razorpay product claims.
2. Label company-reported performance numbers as claims.
3. Never invent statistics.
4. If uncertain: write "I could not verify this from an authoritative source."

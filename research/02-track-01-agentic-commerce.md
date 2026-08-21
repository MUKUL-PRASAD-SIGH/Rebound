# 02 — Track 01: AI Growth & Agentic Commerce

> Status: researched (first pass) · Shortlist candidate with caveats · Not selected yet

## What the track asks

From the [official page](https://razorpay.com/buildathon/):

Build an agent that either:

1. grows revenue for a merchant on Razorpay **test-mode** APIs, **or**
2. makes a merchant **transactable by an AI buyer** end to end.

Example directions they list: conversational in-app checkout, agent-readable catalog, upsell/cross-sell agent, campaign orchestrator.

Why-now language on the page: NPCI’s UAP and the global protocol race (ACP, AP2, x402); Razorpay’s in-app pilots already live.

## What I thought at first

"Agentic commerce is the hottest theme of 2026. Build a chat checkout that pays with Razorpay."

That instinct is exactly how you accidentally rebuild a press demo.

## What Razorpay already provides / is piloting

| Capability | What it is | Source | Implication for this track |
| --- | --- | --- | --- |
| **Agentic Payments** | Payments inside AI-native journeys (in-app, LLM chat, voice) | [razorpay.com/agentic-payments](https://razorpay.com/agentic-payments/) | Core rails for conversational checkout already exist as a product direction |
| **UPI Reserve Pay** | Consent once, set spend limit, multiple debits within bounds (NPCI SBMD) | [UPI Reserve Pay blog](https://razorpay.com/blog/upi-reserve-pay/) · marked Live on Agentic Payments page | Bounded agent spend is a solved *rail*, not an open invention |
| **Claude pilot (Feb 20, 2026)** | Shop via Claude with Zomato / Swiggy / Zepto; pilot / closed user group | [Agentic Payments & NPCI blog](https://razorpay.com/blog/agentic-payments-and-npci/) · [Newsroom](https://razorpay.com/newsroom/razorpay-npci-launch-agentic-payments-on-claude-powering-zomato-swiggy-zepto-at-the-india-ai-impact-summit/) | End-to-end "AI buyer pays" is being productized with big brands |
| **ChatGPT / OpenAI line** | Agentic payments on ChatGPT (private beta history); Codex + MCP monetization | [ChatGPT agentic payments blog](https://razorpay.com/blog/razorpay-unveils-agentic-payments-on-chatgpt-with-npci-indias-first-ai-powered-conversational-payment-experience/) · [Codex newsroom](https://razorpay.com/newsroom/razorpay-launches-upi-and-all-payment-methods-within-openais-codex-enabling-developers-to-build-and-monetise-apps-instantly/) | LLM surfaces are a Razorpay strategic bet, not a blank canvas |
| **Voice agentic commerce** | Voice-driven flows with partners (e.g. SuperU mentioned in Reserve Pay blog) | [UPI Reserve Pay blog](https://razorpay.com/blog/upi-reserve-pay/) | Voice checkout demos will look familiar to judges |
| **Razorpay MCP Server** | Official MCP tools for AI agents to call Razorpay APIs | [GitHub razorpay/razorpay-mcp-server](https://github.com/razorpay/razorpay-mcp-server) | Good building block; wrapping MCP alone is not a product |

### Realization

Razorpay is not asking "please invent agentic payments." They are asking builders to explore **growth and merchant-side sellability to AI buyers** in a world where the payment rail is already moving.

If I ship another "chat → pay" demo without a sharp merchant problem, I am competing with Razorpay's own Sprint / GFF / AI Summit storytelling.

## What changes because of Vulcan (Aug 2026)

[Vulcan](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/) is a payments foundation model for routing, fraud, and checkout personalization (company-reported early results; proprietary).

That changes Track 01 evaluation like this:

- Naive "AI picks the best payment method at checkout" overlaps with Vulcan's checkout personalization story.
- Naive "AI routes the payment for success" overlaps with hyper-precision routing.
- A student project will not out-data Vulcan.

So the interesting student-shaped gaps are more likely on the **merchant / catalog / protocol / orchestration** side than on core payment intelligence.

## Where a hackathon project might still add something

Hypotheses worth testing (not claims):

1. **Agent-readable catalog / offer graph**  
   Make a merchant's products, constraints, inventory, and policies machine-consumable so an AI buyer can transact without brittle scraping. Razorpay is pushing agent-led checkout; many merchants are not agent-ready.

2. **Bounded merchant-side growth agent**  
   Upsell / cross-sell / campaign orchestration that proposes actions, runs through allowlists + spend/discount caps, executes via test-mode payment links / offers, and measures incremental conversion — not "LLM spams coupons."

3. **Protocol adapter layer**  
   Track mentions ACP / AP2 / x402 / UAP. Bridging a merchant catalog into an agent-commerce protocol *could* be differentiation — **but** I have not yet verified which of these are stable enough to demo honestly.  
   **TODO:** primary docs for UAP / ACP / AP2 / x402 before betting the project on them.

## Flashy vs real

| Idea | Flashy? | Real product potential? | Overlap risk |
| --- | --- | --- | --- |
| Chat checkout that "just pays" | High | Low differentiation | Very high |
| Voice order demo | High | Medium (rail exists) | High |
| Agent-readable catalog + policy guardrails | Medium | Higher | Medium-low |
| Upsell agent with incremental lift metric | Medium | Medium | Medium (marketing tools exist) |
| Protocol bridge without merchant value | Medium | Unclear | Spec risk |

## Fit with my skills

Strong: agents, RAG over catalogs, APIs, FastAPI + React demo, guardrail architecture.  
Weak relative to big-brand demos: access to live Reserve Pay / production agentic surfaces (likely simulated / test-mode / mocked consent).

## ₹0 / test-mode notes

- Test-mode Orders / Payments / Payment Links are the realistic path.
- Reserve Pay / live Claude shopping is **not** something I should pretend to have in production.
- Clearly label: simulated AI-buyer flow vs real Razorpay test transactions.

## Current verdict on Track 01

**Keep on shortlist only if the thesis is merchant-side agent-readiness or bounded growth orchestration — not "we rebuilt Agentic Payments."**

Otherwise reject as demo-theater.

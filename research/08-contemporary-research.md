# 08 — Contemporary Research (why 2026 changes the problem space)

> Each item: what happened → why it changes how I evaluate tracks.  
> Dates from primary/credible sources. Claims that are company-reported are marked as such.

## 1) Vulcan — AI Payments Foundation Model (Aug 2026)

**What:** Razorpay announced Vulcan as India’s payments foundation model (transformer-based, payments-domain; **not** a chatbot LLM). Built with NVIDIA + AWS/SageMaker. Trained on large proprietary payments data (company figures: on the order of trillions of data points / billions of payments — see sources).

**Primary:** [Razorpay blog — One Foundation Model…](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)  
**Also:** AWS press (18 Aug 2026), Fortune India coverage.

**Company-reported effects (not independently audited here):** success-rate lift, fraud detection improvements, checkout personalization (e.g. preferred UPI app surfacing). Treat as vendor claims.

### Why this changes the problem space

- Track 02: a generic fraud model is competing with a network-scale foundation story.
- Track 01: "AI picks payment method" / "AI routes better" overlaps Vulcan's stated jobs.
- Track 03: payment *success* intelligence is consolidating inside Razorpay; recovery decisioning at merchant-policy level is a different layer.

**Project implication:** stay above Vulcan. Do not try to recreate payment foundation intelligence.

## 2) Agentic Payments with NPCI (2025→2026 pilots)

**What:** Razorpay + NPCI enable AI agents to complete purchases under consent frameworks, demonstrated across ChatGPT / Gemini / Claude narratives and brand pilots (food, grocery, telecom, etc.).

**Primary examples:**

- [Agentic Payments & NPCI (Claude, 20 Feb 2026)](https://razorpay.com/blog/agentic-payments-and-npci/)
- [ChatGPT agentic payments blog](https://razorpay.com/blog/razorpay-unveils-agentic-payments-on-chatgpt-with-npci-indias-first-ai-powered-conversational-payment-experience/)
- [Agentic Payments product](https://razorpay.com/agentic-payments/)

### Why this changes the problem space

Track 01 is strategically central — and crowded by Razorpay's own demos.  
The open student problem is less "can AI pay?" and more "what must a merchant become for AI buyers / what growth loops sit on these rails?"

## 3) UPI Reserve Pay (Live) + UPI Circle (Coming soon)

**What:** Reserve Pay (NPCI SBMD-based) lets users authorize a merchant spending capacity; agents/platforms debit within bounds without repeated PIN theater. Users retain visibility/revocation.

**Primary:** [UPI Reserve Pay blog](https://razorpay.com/blog/upi-reserve-pay/) · Agentic Payments page marks Reserve Pay **Live**, UPI Circle **Coming soon**.

### Why this changes the problem space

Bounded autonomy is now a **payments primitive**.  
Any agent project that moves money without spending limits, revocation, and audit is architecturally behind the ecosystem.

## 4) Agent Studio (FTX 2026)

**What:** Marketplace of operational AI agents inside Razorpay (Claude Agent SDK). Launch agents include dispute response, subscription recovery, abandoned cart conversion, cashflow forecasting, etc.

**Primary:**

- [Newsroom — Agent Studio at FTX’26](https://razorpay.com/newsroom/razorpay-launches-the-worlds-first-ai-native-agent-studio-for-payments-at-ftx26-powered-by-anthropics-claude/)
- [Principles, guardrails, merchant control](https://razorpay.com/blog/razorpay-agent-studio-principles-guardrails-and-merchant-control/)
- [Agent Studio](https://razorpay.com/agent-studio/)

### Why this changes the problem space

Tracks 02/03/04 example directions partially map onto Agent Studio SKUs.

**Project implication:** differentiate on decision quality, evaluation, policy engines, and measurable incremental outcomes — or pick a niche Agent Studio does not already pitch.

Also: Razorpay publicly emphasizes merchant control and guardrails. That is a hint for judging taste.

## 5) Intelligent Retry Engine / Revenue-Protect (FTX 2026)

**What:** Configurable retry strategies for Autopay failures; WhatsApp recovery links/reminders as part of a broader revenue-protect stack.

**Primary:** [UPI Autopay with Intelligent Revenue-Protect](https://razorpay.com/blog/upi-autopay-with-intelligent-revenue-protect/) · listed on [Sprint 2026](https://razorpay.com/sprint/26)

### Why this changes the problem space

Track 03's obvious "smart retry" idea is product-adjacent.  
The remaining gap is closer to **intervention selection under economic constraints** across multiple failure modes (not only Autopay timing).

## 6) Razorpay MCP + Codex monetization (Apr 2026)

**What:** Official MCP server; payments inside OpenAI Codex workflows; ChatGPT app management themes.

**Primary:** [Codex newsroom (6 Apr)](https://razorpay.com/newsroom/razorpay-launches-upi-and-all-payment-methods-within-openais-codex-enabling-developers-to-build-and-monetise-apps-instantly/) · [MCP GitHub](https://github.com/razorpay/razorpay-mcp-server)

### Why this changes the problem space

Builder interface to Razorpay is becoming agent-native.  
A project that only wraps MCP without a sharp problem is weak. A project that uses MCP/tools as execution hands for a real decision system is aligned.

## 7) Broader Indian fintech / NPCI direction

**Verified enough for research notes:** NPCI is actively enabling consent frameworks that make agentic debit possible (Reserve Pay / related UPI capabilities). India has unusual payments readiness for agent commerce relative to many markets.

**TODO:** pull primary NPCI/RBI circulars for any regulatory claim I later assert in public writeups. Do not overclaim regulation from Razorpay blogs alone.

## 8) Global adjacent pattern (subscriptions)

Stripe and third-party dunning tools show a layered recovery market: processor retries ≠ full recovery stack.

**Why it matters:** supports the hypothesis that "decision + communication + measurement above retries" is a real category — while reminding me Razorpay is racing into that category too.

## Net effect on my shortlist

| Development | Pushes me toward | Pushes me away from |
| --- | --- | --- |
| Vulcan | Layers above core payment IQ | DIY fraud/routing/checkout IQ |
| Agentic Payments + Reserve Pay | Merchant-side agent-readiness; bounded action design | Vanilla chat-checkout demos |
| Agent Studio recovery/dispute agents | Better evaluation + EV policy differentiation | Cloned recovery/dispute UX |
| Intelligent Retry Engine | Cross-intervention decisioning | Retry-timing-only projects |
| MCP | Tool-using agents with real API boundaries | Prompt-only demos |

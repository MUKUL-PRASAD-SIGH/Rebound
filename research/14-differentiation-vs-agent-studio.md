# Differentiation vs Agent Studio Subscription Recovery

> Locked note — 21 Aug 2026. Keeps Rebound from sliding back into “smart retry / voice dunning clone.”

## What Razorpay already covers (baseline reality)

| Capability | Exists? | Source class |
| --- | --- | --- |
| Automatic subscription retries + pending/halted | Yes | Docs |
| Hosted payment-method update / customer email | Yes | Docs |
| Intelligent Retry Engine / Revenue-Protect themes | Yes | Product blog / Sprint |
| Agent Studio Subscription Recovery (nudges, smarter retry logic, voice variants) | Yes | Newsroom / Agent Studio |

## What Rebound owns

| Layer | Rebound | Not Rebound |
| --- | --- | --- |
| Retry timing rails | Compose / respect | Reinvent |
| Voice/WhatsApp novelty | Optional later; not the thesis | Core demo |
| **Intervention selection under EV + cost** | Core | — |
| **Explicit stop / do-not-act** | Core | — |
| **Incremental lift vs fixed baseline** | Core scoreboard | Vanity “recovered” without baseline |
| **Policy/guardrail engine (allowlist, limits, confidence)** | Core | LLM direct charge |
| Audit trail of proposal → gate → action → outcome | Core | — |

## One sentence (use everywhere)

Razorpay retries and Agent Studio run recovery playbooks; Rebound is the **decision layer** that picks the economically right bounded action — including stopping — and proves incremental lift.

## Failure mode to watch

If a commit message or pitch says only “AI retries failed payments,” we have drifted. Rewrite toward EV + policy + measurement.

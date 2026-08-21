# 12 — Final Selection

> **Status: LOCKED — 21 Aug 2026**  
> Track **03 — AI Revenue Recovery**  
> Process story: [`13-how-i-chose-the-ps.md`](./13-how-i-chose-the-ps.md)

## The narrowing

```text
All 5 tracks
    ↓
Read + first-pass notes
    ↓
Landscape research (Vulcan, Agentic Payments, Reserve Pay,
Agent Studio, retries, Intelligent Retry, X accounting)
    ↓
Rejected clones (smart retry, chat-pay, generic fraud,
dispute-bot, settlement chatbot)
    ↓
Shortlist: T03 decision layer · T01 merchant-readiness · T04 backup
    ↓
LOCKED: Track 03 — expected-value revenue recovery controller
```

## Final choice

**Track:** 03 — AI Revenue Recovery  
**Working title:** Rebound  
**Thesis type:** Decision-intelligence layer above Razorpay recovery rails — **not** “AI payment retry.”

## Differentiation (one sentence)

> Razorpay already retries and Agent Studio already runs recovery playbooks; **Rebound** decides *whether* revenue is worth recovering, *which* bounded intervention maximizes expected value under cost/policy limits (including stop), executes only allowlisted actions via Razorpay-compatible workflows, and reports **incremental** recovered value vs a fixed baseline with a full audit trail.

## Final problem statement

Subscription and checkout revenue rarely dies in one clean failure. It degrades across failed charges, stale payment methods, customer inaction, and recovery efforts that either under-react or over-spend. Razorpay already provides retries, webhooks, hosted payment-method updates, and agent-style recovery products — but merchants still need a measurable decision layer that chooses the economically right bounded action (including when not to act). Rebound is that controller: detect revenue at risk → estimate recoverability and intervention value → enforce guardrails → act through test-mode Razorpay workflows → measure incremental lift.

## Final project thesis

> We believe that revenue recovery can be improved by an expected-value decision layer above Razorpay’s existing retry and payment-update workflows, resulting in higher incremental recovered revenue under explicit cost, retry, and communication constraints — with a full audit trail.

## Why now / why Razorpay / why me / why AI

| Question | Answer |
| --- | --- |
| Why now? | Agentic era + Intelligent Retry + Agent Studio make naïve retries obsolete; the buildathon scores measured recovery, stopping rules, audit |
| Why Razorpay? | Execution rails + the competitive baseline both live here |
| Why me? | Tabular ML + agents + FastAPI/React + eval harness — end-to-end systems fit |
| Why AI? | Heterogeneous P(recover)/P(respond) + structured action proposals beat fixed dunning *if* they beat a strong baseline (we’ll measure either way) |

## Locked build path (Aug 21 decision — detail on Aug 22)

| Piece | Choice |
| --- | --- |
| Primary failure domain | Failed subscription / recurring-style charges (+ optional checkout abandonment later) |
| Razorpay surfaces (test-mode) | Webhook-shaped events, subscriptions/invoices where usable, **Payment Links** as recovery action, dashboard/API reads |
| What we simulate | Outreach channels (email/WhatsApp/voice logged, not faked as delivered); some failure labels in synthetic batch |
| What we never pretend | Test-mode ₹ = real money |
| Baseline to beat | Fixed policy (e.g. always retry N times → always send update link → stop) |
| North-star metric | Incremental recovered value vs baseline on a held-out batch |
| Safety | Model proposes → policy engine gates → allowlisted execute → audit |

## Why not the others (locked)

| Track | Decision |
| --- | --- |
| 01 Agentic Commerce | Strong, but demo-collision with Agentic Payments; revisit only if Rebound blocks |
| 02 Risk Manager | Parked — data + Vulcan/SHIELD overlap |
| 04 Finance Controller | Backup only |
| 05 Open | Unused |

## Assumptions rejected

| Assumption | Outcome |
| --- | --- |
| Razorpay lacks retries | False |
| Agentic checkout is empty land | False |
| Fraud is the obvious ML flex | Too risky for honest data |
| Voice recovery = differentiation | Agent Studio already markets it |
| Need Open Track for originality | False |

## Aug 21 complete → Aug 22

Research-as-selection is **done**.  
Tomorrow: problem decomposition + architecture + MVP scope only.  
No more domain browsing for sport.

# 13 — How I Chose the Problem Statement

> **Rule:** I made the decision. Tools challenged, validated, and deepened the reasoning — they did not pick for me.  
> **Status: LOCKED — Track 03 / Rebound — 21 Aug 2026**

## Framing

After going through all the problem statements, I didn't want to immediately pick the one that sounded the most technically impressive. I wanted to understand what each problem was actually asking, how deep the underlying problem was, what could realistically be built within the buildathon timeline, and where I could contribute something beyond a basic implementation.

I therefore treated the selection itself as a small research exercise:

```text
Read everything
    → form my own initial understanding
    → use research/AI tools to challenge that understanding
    → research the surrounding problem + Razorpay ecosystem
    → compare the PSs
    → check fit with what I actually enjoy building
    → choose the one I genuinely find interesting
```

---

## 1. First-pass understanding (before AI analysis)

I personally read every track on the [official Buildathon page](https://razorpay.com/buildathon/) and made initial notes **before** treating any model output as authority.

| Question | Why I asked it |
| --- | --- |
| What is the actual problem? | Strip marketing language |
| Who experiences it? | Merchant? buyer? finance ops? risk team? |
| Why does it matter? | Severity vs demo fluff |
| What would a naïve solution look like? | So I can reject clones later |
| What could make a solution genuinely different? | Differentiation under time pressure |
| What would be difficult to implement? | Feasibility |
| What could realistically be demonstrated? | Judging / internship signal |

| Track | Actual problem (my read) | Naïve solution I'd avoid | What "different" might mean |
| --- | --- | --- | --- |
| **01 Agentic Commerce** | Growth + sellability to AI buyers | Chat checkout that "just pays" | Merchant-side agent-readiness |
| **02 Risk Manager** | Fraud / returns / chargebacks | Generic fraud classifier | Narrow loss class + FP-cost honesty |
| **03 Revenue Recovery** | Revenue slips across failures & abandonment | "AI smart retries" | Whether / which / when — including stop |
| **04 Finance Controller** | Manual finance ops | Settlement chatbot | Exception-first closed loop |
| **05 Open** | Escape hatch | Random fintech chatbot | Only if it beats a defined track |

---

## 2. Multi-model / research-tool analysis

| Tool | Job | Contribution | Status |
| --- | --- | --- | --- |
| My notes | Own understanding | Baseline questions + naïve traps | Done |
| ChatGPT | “What am I overlooking?” | Structured challenge of assumptions | Done — keep transcript private |
| Cursor + primary sources | Landscape vs Razorpay docs/newsroom | Forced confrontation with retries, Agent Studio, Vulcan, Agentic Payments | Done — this `research/` folder |
| Claude / NotebookLM / Gemini | Extra challenge passes | Nice-to-have evidence | **Deferred** — schedule > tool tourism; run only if a concrete Aug 22 question needs them |

---

## 3. Research beyond the PS

Razorpay’s 2026 direction (Agent Studio, Agentic Payments, Reserve Pay, MCP) reframed the question from “can I build an agent?” to:

> Where does my solution fit — and what should an agent be **allowed** to do?

See [`07`](./07-razorpay-landscape.md), [`08`](./08-contemporary-research.md), [`14`](./14-differentiation-vs-agent-studio.md).

---

## 4. Why this PS interested me

I've been working across AI/ML, RAG, multi-agent systems, MCP-style tooling, and backends. I wasn't looking for a place to bolt on an LLM. I wanted intelligence, orchestration, and **bounded actions** to change a real workflow.

Track 03 — as **decision intelligence for recovery** — is that intersection. I can imagine working on it after the deadline. That mattered.

---

## 5. Why I didn't choose the others

| PS | What interested me | Main concern | Final decision |
| --- | --- | --- | --- |
| 01 — Agentic Commerce | Strategic heat | Demo-collision with Razorpay pilots | Not selected |
| 02 — Risk Manager | ML fit | Data + product overlap | Not selected |
| **03 — Revenue Recovery** | Measurable ₹ + decisioning | Must not become retry clone | **SELECTED** |
| 04 — Finance Controller | Clean scoreboard | Shallow dashboard risk | Not selected |
| 05 — Open | Freedom | Weaker than defined track | Not selected |

---

## 6. Decision

The choice was the intersection of problem significance, technical depth, feasibility, differentiation, personal interest, and skill fit.

**Locked:** Track 03 → project **Rebound**  
Details: [`12-final-selection.md`](./12-final-selection.md) · Overview: [`docs/00-project-overview.md`](../docs/00-project-overview.md)

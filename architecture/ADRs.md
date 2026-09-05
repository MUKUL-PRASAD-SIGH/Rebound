# Architecture Decision Records (light)

## ADR-001 — SQLite for MVP storage

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Use SQLite for local MVP; keep SQLAlchemy models Postgres-friendly.  
- **Alternatives:** Postgres from day one, MongoDB.  
- **Why:** ₹0, zero ops, fastest path to Aug 26. Migrate if deploy needs it.

## ADR-002 — Policy engine is deterministic and mandatory

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Every action passes a pure policy function before execute.  
- **Alternatives:** Trust model output; soft warnings only.  
- **Why:** Money-adjacent actions; judging bar wants stopping rules + audit; matches Agent Studio “merchant control” taste without cloning it.

## ADR-003 — No agent framework for MVP

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Plain Python modules + optional single LLM JSON call. No LangGraph/CrewAI.  
- **Alternatives:** Full multi-agent graph.  
- **Why:** Schedule rule against framework tourism; loop is linear enough.

## ADR-004 — Payment Link as primary live recovery action

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** MVP mode (Razorpay Test Mode) Payment Links are the main real Razorpay side effect in MVP.
- **Alternatives:** Direct subscription charge only; invoices only.  
- **Why:** Clear demo artifact (URL/id); fits “bounded recovery workflow”; works when full subscription retry APIs are awkward in sandbox.

## ADR-005 — Outreach is simulated in MVP

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Email/WhatsApp/voice = audit log + `simulated` label, not provider sends.  
- **Alternatives:** Twilio/WhatsApp Cloud API.  
- **Why:** ₹0, honesty, avoid fake delivery metrics; differentiation is decisioning not channel novelty.

## ADR-006 — Baseline-first evaluation

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Every eval run compares Rebound to Baseline A on the same batch.  
- **Alternatives:** Only show Rebound recoveries.  
- **Why:** Prevents vanity metrics; enforces thesis of incremental lift.

## ADR-007 — Dual proposer: rules default, LLM optional

- **Date:** 2026-08-22  
- **Status:** Accepted  
- **Decision:** Ship with rules/EV proposer on by default; LLM proposer behind feature flag.  
- **Alternatives:** LLM-only decisions.  
- **Why:** Demo must work offline/without keys; LLM adds diagnosis text + structured suggestions, not authority.

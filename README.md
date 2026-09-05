# Rebound — Razorpay AI Buildathon 2026

[![Track](https://img.shields.io/badge/Track-03%20AI%20Revenue%20Recovery-0A2540?style=for-the-badge)](https://razorpay.com/buildathon/)
[![Status](https://img.shields.io/badge/Status-Demo--ready%20MVP-2E7D32?style=for-the-badge)](#validation-and-scope)
[![MVP Mode](https://img.shields.io/badge/MVP%20Mode-Razorpay%20Test%20Mode-136FEC?style=for-the-badge)](#mvp-mode-functional-testing-without-production-money)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%C2%B7%20ML%20%C2%B7%20React-136FEC?style=for-the-badge)](#technology)

<p align="center">
  <strong>Research-backed, expected-value decision intelligence for revenue recovery.</strong><br/>
  Detect at-risk revenue &rarr; choose bounded interventions &rarr; execute through Razorpay-compatible workflows &rarr; measure incremental lift against a baseline
</p>

<p align="center">
  <a href="https://razorpay.com/buildathon/"><img src="https://img.shields.io/badge/Razorpay-AI%20Buildathon%202026-072654?logo=razorpay&logoColor=white" alt="Razorpay Buildathon" /></a>
  <img src="https://img.shields.io/badge/Workspace-private%20by%20default-136FEC" alt="Private operator workspace" />
</p>

---

## What I built

**Rebound** is a recovery-operations console for failed payments. It is not another blind-retry bot: it helps a merchant team decide whether recovery is worth attempting, which bounded action has the highest expected value, and when the correct answer is to stop or escalate.

| Product capability | What it does |
| --- | --- |
| Recovery queue | Loads and prioritises failed-payment cases in one operations view. |
| Expected-value engine | Scores recoverability, intervention cost, and the expected value of each action. |
| Structured intelligence | Uses an optional schema-constrained LLM proposer with a deterministic local EV fallback. |
| Deterministic policy gate | Applies action allowlists, confidence floors, retry caps, stopping rules, and escalation rules. |
| Safe execution | Runs dry-run and simulated flows by default, with a guarded **MVP mode** Payment Link flow backed by Razorpay Test Mode. |
| Evaluation lab | Compares Rebound with Baseline A and Baseline B on the same synthetic portfolio. |
| Audit trail | Records the score, proposal, policy decision, execution, and outcome for every case. |
| Private operator dashboard | A polished, payment-operations interface inspired by familiar Razorpay workflow patterns—without copying Razorpay branding or exposing customer data. |

## Users and user stories

Rebound is built for the person who opens a recovery queue each morning and must decide what should happen next—not merely for someone looking at a payment dashboard. Its primary workflow is: **prioritise money at risk → choose an intervention (or stop) → apply controls → review the result**.

| Persona | Job to be done | How the MVP helps |
| --- | --- | --- |
| Payment / Revenue Operations Manager | Focus the team on failed payments that are worth recovering. | Ranks the recovery queue using recoverability and expected value. |
| Recovery Operations Analyst | Decide the most appropriate next action for each case. | Recommends retry, Payment Link, update-method outreach, escalation, or `stop`, then shows the policy result. |
| Merchant / Finance Manager | Establish whether a recovery policy adds value beyond the current approach. | Compares Rebound with fixed baselines on the same portfolio using a paired simulated net-value delta. |

### MVP user stories

1. **Prioritise recovery work** — *As a payment operations manager, I want failed-payment cases ranked by expected recovery value so that the team works on the most valuable opportunities first.*
2. **Choose a proportionate action** — *As a recovery analyst, I want a recommendation to retry, send a Payment Link, request a payment-method update, escalate, or stop so that each case gets the most appropriate intervention.*
3. **Know when not to act** — *As a merchant, I want Rebound to identify recovery attempts that are economically irrational so that I avoid unnecessary cost and customer friction.* The first-class `stop` decision is central to Rebound's differentiation.
4. **Keep AI money-adjacent actions bounded** — *As a risk-conscious operator, I want every AI proposal to pass deterministic policy checks before execution so that a model cannot independently trigger an unsafe action.*
5. **Explain each decision** — *As an operations manager, I want to see why an action was proposed, approved, rejected, or stopped so that I can review and trust the system.*
6. **Handle exceptions safely** — *As a recovery team member, I want uncertain or high-value cases marked for escalation so that they can receive human review.* In this MVP, escalation is an auditable handoff signal, not an integrated staffed-workflow or approval system.
7. **Measure incremental value** — *As a merchant, I want to compare Rebound with my existing recovery policy so that I can assess whether the new automation adds value beyond what would have happened anyway.*

These stories are demonstrated on the seeded synthetic portfolio and, where configured, Razorpay Test Mode—not on production merchant outcomes.

## Why it is research-backed

The research started from an uncomfortable product reality: Razorpay already offers retry rails and AI recovery capabilities. A useful build therefore cannot merely claim to “retry smarter.” Rebound is deliberately designed as the **measurable decision layer above those rails**.

- **Economic decisioning, not generative guessing:** each intervention is evaluated with recoverability, cost, expected value, and a first-class `stop` option.
- **Constrained autonomy:** a model can propose only a structured candidate; deterministic policy is the final authority over every money-adjacent action.
- **Baseline-controlled measurement:** the headline is the paired difference against a fixed recovery policy, not a vanity count of “recovered” cases.
- **Operational traceability:** every proposal, gate result, execution attempt, and outcome is retained for explanation and review.

> **Differentiation:** retries and recovery playbooks run actions; Rebound decides *whether / which / when*—including **stop**—and measures the incremental result against a fixed baseline.

The full problem selection, competitive analysis, baseline rationale, and source list are available in the [research index](research/README.md), especially [the locked product decision](research/12-final-selection.md) and [the differentiation analysis](research/14-differentiation-vs-agent-studio.md).

## How it works

| Step | What happens |
| --- | --- |
| 1 | Detect revenue at risk from failed-payment or recovery signals |
| 2 | Estimate recoverability and intervention expected value |
| 3 | Propose a structured action: retry signal, Payment Link, update-method outreach, stop, or escalate |
| 4 | Enforce **deterministic guardrails**: allowlists, caps, confidence floors, and stopping rules |
| 5 | Execute only allowlisted Razorpay-compatible workflows in dry-run, simulated, or explicit MVP mode |
| 6 | Report **incremental simulated net-value delta versus Baseline A** with a full audit trail |

## How this could help Razorpay

Rebound is designed as a complement to Razorpay’s payment rails—not a replacement for them. With merchant-approved production data and controls, it could become a policy and measurement layer that:

1. selects the least-cost, highest-value recovery intervention across retries, hosted payment-method updates, Payment Links, and human escalation;
2. gives merchants clear safety controls, explanations, and an audit record for each recommendation;
3. measures incremental lift against a merchant’s existing recovery policy, so teams can see whether automation is genuinely adding value; and
4. creates a feedback loop for safe experimentation and later model calibration from observed outcomes.

That is the product direction—not a claim that this MVP has already achieved production lift.

## Technology

| Layer | Choice |
| --- | --- |
| API | FastAPI |
| Intelligence | Rules + expected value; sklearn/logistic model; optional OpenAI structured proposer |
| Policy | Mandatory deterministic Python engine |
| UI | React + TypeScript |
| Data | SQLite + SQLAlchemy |
| Payments | Razorpay standard Payment Links in MVP mode (Razorpay Test Mode) |
| Frameworks | No agent framework in the decision-critical path |

Architecture: [system design](architecture/README.md) · [MVP scope](architecture/mvp-scope.md) · [API surface](architecture/api-surface.md)

---

## Validation and scope

This table is the honest status of the locked build path.

| Locked goal | Status | Evidence / boundary |
| --- | --- | --- |
| Failed subscription / recurring-style recovery as the primary domain | **Met for the synthetic MVP** | The seeded portfolio models failed-payment recovery. Direct subscription or invoice reads are a next integration, not a shipped claim. |
| Razorpay MVP-mode surfaces | **Functionally complete; account proof pending** | The executor creates a standard Razorpay Test Mode Payment Link, records it as pending, verifies raw-body webhook signatures, and reconciles a signed `payment_link.paid` event. A real account run and dashboard/API read integration still need to be demonstrated. |
| Outreach and some failure labels simulated—not faked as delivered | **Met** | Outreach is an explicitly labelled audit-log simulation. |
| Never present MVP-mode or simulated value as real money | **Met** | UI/docs use `simulated_net_value_delta`; creating a link does not count as recovery. Only the signed MVP mode (Razorpay Test Mode) paid webhook can close its case. |
| Fixed policy baseline | **Met** | Evaluation runs Baseline A, Baseline B, and Rebound on the same seeded portfolio. |
| Incremental recovered value on a held-out batch | **Partially met** | The product calculates paired **synthetic** net-value delta. It is not yet an independent held-out merchant dataset or production ROI. |
| Model proposes → policy gates → allowlisted execution → audit | **Met** | The policy engine remains mandatory; the optional LLM can never execute an action directly. |

The current backend regression suite passes; the release record also contains a passing production frontend-build check. The remaining high-value proof is one controlled Razorpay **MVP-mode** Payment Link creation/payment and a signed webhook delivery to a public test endpoint. Do not present that proof as real merchant recovery.

## Future scope

The MVP demonstrates a safe decision architecture; it does **not** claim the following capabilities as shipped. This is the path from a credible buildathon prototype to a merchant-ready product.

| Future capability | Current boundary | What would be needed |
| --- | --- | --- |
| End-to-end external integration proof | Payment Link creation, status refresh, and signed-webhook reconciliation are implemented for Razorpay Test Mode, but a controlled account run has not been recorded. | Run and document an authorised Test Mode payment success/failure with a public signed-webhook delivery. |
| Direct subscription and invoice recovery ingestion | Read-only Test Mode subscription/invoice endpoints exist, but they do not yet automatically normalise merchant objects or lifecycle events into recovery cases. | Merchant-authorised event ingestion, mapping, reconciliation, and lifecycle handling. |
| Real customer outreach | `notify_update_method` is explicitly an audit-log simulation; Rebound does not send email, WhatsApp, voice, or SMS. | Consent-aware provider integrations, templates, opt-out handling, delivery/outcome tracking, and rate limits. |
| Human approval operations | `escalate` records a controlled handoff signal only. There is no assignee, approval queue, SLA, or case-management integration. | Role-based approval workflows, assignment, queues, notifications, and resolution tracking. |
| Real-data model calibration | The current scoring and evaluation are designed for a synthetic portfolio. | Consented merchant history, calibration and reliability testing, drift monitoring, and an outcome-feedback loop. |
| Independent evidence of merchant value | `simulated_net_value_delta` is a paired synthetic measure, not production recovery uplift or ROI. | A pre-registered hold-out or controlled merchant evaluation against the merchant's existing policy. |
| Recovery Policy Lab | The evaluator compares Rebound with fixed Baseline A and Baseline B; it is not a merchant-configurable experimentation product. | Configurable policy variants, experimentation safeguards, cohort controls, and observed-outcome analysis. |
| Broader recovery coverage | The MVP focuses on failed-payment / recurring-style recovery cases. | Support for checkout abandonment and additional payment-lifecycle signals after validating the core workflow. |
| Production operation and live execution | Live Razorpay keys and production actions are deliberately rejected; the app is local, single-operator, and Test Mode first. | Merchant authorisation, multi-tenant RBAC/SSO, managed secrets, durable storage, monitoring, incident controls, privacy/compliance review, and change management before any live action. |

Until those items are complete, Rebound should be described as **a safe, measurable decision architecture for payment recovery**, not as proven production recovery automation or real merchant ROI.

## Safety and secrets

- Never commit `.env`, API keys, webhook secrets, or personal data.
- Start from [`.env.example`](.env.example); the default mode is offline `dry_run`.
- All operator routes require `REBOUND_API_TOKEN`; the browser keeps it only in session storage and never displays it.
- Customer references are pseudonymised before storage. API responses redact credentials, contact data, URLs, notes, and upstream Razorpay fields that are not needed for operations.
- LLM proposals are schema-constrained, exclude customer identifiers, and fall back to the local EV proposer on any failure.
- Model **proposes** → policy engine **gates** → allowlisted executor runs → audit is recorded.
- MVP-mode and synthetic outcomes are always labelled honestly; simulated ₹ are not real revenue.

Security design and verification notes: [security posture](docs/SECURITY.md).

### Cybersecurity research summary

Rebound’s controls were designed against the [OWASP API Security Top 10](https://owasp.org/www-project-api-security/), the [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html), and Razorpay’s [webhook validation and idempotency guidance](https://razorpay.com/docs/webhooks/validate-test/?preferred-country=IN). The resulting MVP controls are deliberately concrete:

| Research concern | Rebound response |
| --- | --- |
| Unauthorised API access and object exposure | A local operator token protects every non-webhook route; the UI never receives raw customer references. |
| Excessive data exposure | Customer references are HMAC-pseudonymised; audit and Razorpay responses are redacted or field-allowlisted before reaching the dashboard. |
| Secret leakage | Keys remain in the untracked local `.env`; the browser never embeds or displays them, and the release checklist scans tracked files. |
| Forged or duplicate payment events | Razorpay webhook HMAC is verified against the raw body and the unique event ID is deduplicated. |
| Unsafe third-party payment calls | Live Razorpay keys are rejected; only allowlisted Test Mode operations are available in MVP mode. |

This is security-focused MVP engineering, not a production-security certification. The full research-to-control mapping, verification evidence, and remaining production controls are in [docs/SECURITY.md](docs/SECURITY.md).

---

## Run locally

### Install once

```bash
python -m pip install -r requirements.txt
cd src/apps/web && npm install
```

### Start the app

Before starting, copy `.env.example` to `.env` and replace the two `REBOUND_...` placeholder values with separate random strings. For example:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Use the first value for `REBOUND_API_TOKEN` and the second for `REBOUND_PII_HASH_SALT`.

> **Operator access token:** Rebound does not provide a default token. The value you set for `REBOUND_API_TOKEN` in your local `.env` is the token requested by the private access screen. After starting the app, copy that exact value into **Operator access token**. It remains only for the current browser session; do not commit or share your `.env` file.

Use two terminals from the repository root:

```bash
# terminal 1
make api

# terminal 2
make web
```

> GNU Make is optional on Windows. Use the direct commands below if it is unavailable.

```bash
# terminal 1 — API
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000

# terminal 2 — web
cd src/apps/web && npm run dev
```

Open http://127.0.0.1:5173 — Vite proxies `/api` to the backend.

### Useful checks

```bash
make test
make seed
make eval
```

- Health: http://127.0.0.1:8000/api/v1/health
- Seed: `POST /api/v1/ingest/synthetic` or `make seed`
- Eval: `python src/scripts/run_eval.py`
- Tests: `cd src && python -m pytest tests -q`

## MVP mode: functional testing without production money

**MVP mode** is Rebound’s product environment. Under the hood it uses **Razorpay Test Mode**—Razorpay’s official sandbox name. Rebound has no `production` setting and rejects `rzp_live_` keys before any external call.

| Concern | MVP mode | Production |
| --- | --- | --- |
| Rebound setting | `REBOUND_EXECUTION_MODE=mvp_mode` | Deliberately unsupported |
| Razorpay credentials | `rzp_test_...` Razorpay Test Mode keys | Live keys are rejected |
| Payment Link | Real Razorpay Test Mode link; no real money | Would require merchant approval, live-key controls, monitoring, and compliance work |
| Recovery outcome | Pending until a signed Razorpay Test Mode `payment_link.paid` webhook; synthetic flows remain labelled | Observed merchant outcome with consented data |
| Why | Judges can test the full integration safely and repeatably | Unsafe and dishonest for an unauthorised buildathon demo |

For the buildathon, use MVP mode only. Razorpay supports Payment Links and sandbox success/failure flows in Test Mode; test businesses are limited to 30 Payment Links. See Razorpay’s [Payment Link test guide](https://razorpay.com/docs/payments/payment-links/create/?preferred-country=IN) and [Standard Payment Link API](https://razorpay.com/docs/api/payments/payment-links/create-standard/?preferred-country=IN).

### What a judge needs

| Item | Required? | Purpose |
| --- | --- | --- |
| Python and Node.js | Yes | Run the API and web app |
| `REBOUND_API_TOKEN` | Yes | A locally generated operator token that protects the dashboard and all non-webhook API routes |
| `REBOUND_PII_HASH_SALT` | Recommended | A separate local secret used to pseudonymise customer references at rest |
| No external key | Yes, for dry-run demo | Seed, evaluate, decide, simulate, and inspect audit trails offline |
| `RAZORPAY_KEY_ID` + `RAZORPAY_KEY_SECRET` | Only for an MVP-mode Payment Link | Must be the judge’s own `rzp_test_...` Razorpay Test Mode credentials |
| `RAZORPAY_WEBHOOK_SECRET` + public HTTPS URL | Only for an end-to-end paid-webhook test | Verify Razorpay’s signed delivery; `localhost` cannot receive it |
| `OPENAI_API_KEY` | Optional | Enables the bounded structured LLM proposer; the deterministic proposer needs no key |

No judge should share a secret with this repository or put one in a recording.

Create a local `.env` (never commit it):

```env
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_separate_webhook_secret

REBOUND_EXECUTION_MODE=mvp_mode
REBOUND_API_TOKEN=generate_a_long_random_local_token
REBOUND_PII_HASH_SALT=generate_a_second_random_local_value
REBOUND_ENABLE_LLM_PROPOSER=false
DATABASE_URL=sqlite:///./rebound.db
POLICY_VERSION=mvp-v1
APP_URL=http://localhost:5173
API_URL=http://localhost:8000
```

Then seed a fresh batch, open a case whose gated proposal is `payment_link`, and execute that one case. Rebound creates a standard Razorpay Test Mode Payment Link with notifications and reminders disabled, records it as **pending**, and never exposes its URL in the Rebound UI. Open and complete the link only from the authorised Razorpay dashboard. Avoid bulk MVP-mode execution.

For a genuine webhook check, configure `POST /api/v1/ingest/webhooks/razorpay` on a public HTTPS staging URL or a supported local tunnel, set the same **webhook secret** in Razorpay and `.env`, and subscribe to `payment_link.paid`. Razorpay cannot deliver webhooks to `localhost`; it requires a public URL and signs the raw body with `X-Razorpay-Signature`. Rebound reconciles that event to the original link attempt and marks the case recovered. Follow the [official validation and test guide](https://razorpay.com/docs/webhooks/validate-test/?preferred-country=IN).

If a judge does not want to expose a webhook endpoint, the case screen’s **Refresh payment status** control calls the authenticated Payment Link read API and reconciles its `paid`, `expired`, or `cancelled` state. This is a safe fallback for an MVP-mode demo, although webhooks remain the normal event-driven integration.

MVP mode also exposes these **read-only** endpoints for a judge’s own Test Mode objects:

```text
GET /api/v1/razorpay/subscriptions/{sub_id}
GET /api/v1/razorpay/subscriptions/{sub_id}/invoices
POST /api/v1/cases/{case_id}/refresh-payment-link
```

They require MVP mode and `rzp_test_...` credentials; they reject live keys and never create, cancel, capture, or modify a subscription or invoice.

## Demo flow

1. **Overview** — recovery needs a decision controller, not more blind retries.
2. **Seed batch** — load the repeatable 60-case synthetic portfolio.
3. **Evaluation** — run it *before* batch execution and show Rebound beside Baseline A and Baseline B. Call the metric **simulated net-value delta**, never live revenue.
4. **One case** — preview the proposal, expected value, confidence, and deterministic gate; then decide and execute it safely.
5. **Audit trail** — show the cross-case evidence that makes every decision traceable.

Use a fresh 60-case batch and run Evaluation before bulk execution. Keep terminals and secrets out of the recording, show the `SIMULATED OUTPUT` label, and say “simulated net-value delta”—not live revenue or merchant ROI.

## Documentation map

| Area | Documents |
| --- | --- |
| Product record | [overview](docs/00-project-overview.md) · [research summary](docs/01-research.md) · [ideation](docs/02-ideation.md) · [architecture narrative](docs/03-architecture.md) · [development log](docs/04-development-log.md) · [experiments](docs/05-experiments.md) · [evaluation](docs/06-evaluation.md) · [final results](docs/07-final-results.md) |
| Research record | [complete research index](research/README.md) · [locked selection](research/12-final-selection.md) · [differentiation](research/14-differentiation-vs-agent-studio.md) · [baseline policy](research/15-baseline-policies-draft.md) · [source list](research/sources.md) |
| Technical design | [architecture index](architecture/README.md) — decomposition, scope, system overview, data model, ADRs, and API surface · [security posture](docs/SECURITY.md) |
| Evidence | [benchmark index](evidence/benchmarks/README.md) · [sensitivity notes](evidence/benchmarks/sensitivity.md) · [research-evidence guide](evidence/research/README.md) |
| Build history | [build journal](BUILD_LOG.md) · [day-by-day build log](docs/build-log/README.md) · [documentation system](docs/DOCUMENTATION_SYSTEM.md) |
| Operations and supporting material | [external requirements](docs/EXTERNAL_REQUIREMENTS.md) · [schedule](SCHEDULE.md) · [publish history](docs/WORKER_PUSH_PLAN.md) · [Medium draft](docs/medium-drafts/00-intro-and-series-plan.md) |

## Author

**Mukul Prasad** · CSE, M.S. Ramaiah Institute of Technology, Bengaluru

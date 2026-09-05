# Rebound — Razorpay AI Buildathon 2026

[![Track](https://img.shields.io/badge/Track-03%20AI%20Revenue%20Recovery-0A2540?style=for-the-badge)](https://razorpay.com/buildathon/)
[![Status](https://img.shields.io/badge/Status-Demo--ready%20MVP-2E7D32?style=for-the-badge)](#validation-and-scope)
[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%C2%B7%20ML%20%C2%B7%20React-136FEC?style=for-the-badge)](#technology)

<p align="center">
  <strong>Research-backed, expected-value decision intelligence for revenue recovery.</strong><br/>
  Detect at-risk revenue &rarr; choose bounded interventions &rarr; execute through Razorpay-compatible workflows &rarr; measure incremental lift against a baseline
</p>

<p align="center">
  <a href="https://razorpay.com/buildathon/"><img src="https://img.shields.io/badge/Razorpay-AI%20Buildathon%202026-072654?logo=razorpay&logoColor=white" alt="Razorpay Buildathon" /></a>
  <img src="https://img.shields.io/badge/%E2%82%B90-test--mode%20first-lightgrey" alt="Zero cost build" />
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
| Safe execution | Runs dry-run and simulated flows by default, with guarded Razorpay test-mode Payment Links available when configured. |
| Evaluation lab | Compares Rebound with Baseline A and Baseline B on the same synthetic portfolio. |
| Audit trail | Records the score, proposal, policy decision, execution, and outcome for every case. |

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
| 5 | Execute only allowlisted Razorpay-compatible workflows in dry-run, simulated, or explicit test mode |
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
| Payments | Razorpay standard Payment Links in test mode |
| Frameworks | No agent framework in the decision-critical path |

Architecture: [system design](architecture/README.md) · [MVP scope](architecture/mvp-scope.md) · [API surface](architecture/api-surface.md)

---

## Validation and scope

This table is the honest status of the locked build path.

| Locked goal | Status | Evidence / boundary |
| --- | --- | --- |
| Failed subscription / recurring-style recovery as the primary domain | **Met for the synthetic MVP** | The seeded portfolio models failed-payment recovery. Direct subscription or invoice reads are a next integration, not a shipped claim. |
| Razorpay test-mode surfaces | **Partially met** | The executor can create a standard test-mode Payment Link; the webhook endpoint verifies raw-body signatures and accepts payment/subscription-shaped payloads. A real account run and dashboard/API read integration still need to be demonstrated. |
| Outreach and some failure labels simulated—not faked as delivered | **Met** | Outreach is an explicitly labelled audit-log simulation. |
| Never present test-mode or simulated value as real money | **Met** | UI/docs use `simulated_net_value_delta`; a created link is not counted as a recovered payment. |
| Fixed policy baseline | **Met** | Evaluation runs Baseline A, Baseline B, and Rebound on the same seeded portfolio. |
| Incremental recovered value on a held-out batch | **Partially met** | The product calculates paired **synthetic** net-value delta. It is not yet an independent held-out merchant dataset or production ROI. |
| Model proposes → policy gates → allowlisted execution → audit | **Met** | The policy engine remains mandatory; the optional LLM can never execute an action directly. |

The current backend regression suite passes; the release record also contains a passing production frontend-build check. The remaining high-value proof is one controlled Razorpay **test-mode** Payment Link creation/payment and a signed webhook delivery to a public test endpoint. Do not present that proof as real merchant recovery.

## Safety and secrets

- Never commit `.env`, API keys, webhook secrets, or personal data.
- Start from [`.env.example`](.env.example); the default mode is offline `dry_run`.
- LLM proposals are schema-constrained, exclude customer identifiers, and fall back to the local EV proposer on any failure.
- Model **proposes** → policy engine **gates** → allowlisted executor runs → audit is recorded.
- Test-mode and synthetic outcomes are always labelled honestly; simulated ₹ are not real revenue.

---

## Run locally

### Install once

```bash
python -m pip install -r requirements.txt
cd src/apps/web && npm install
```

### Start the app

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

## Test Razorpay safely (no production mode)

For the buildathon, stay in **Razorpay Test Mode**. You do **not** need live keys, a production account, or real-money charges. Razorpay explicitly supports test Payment Links and test success/failure flows; test businesses are limited to 30 Payment Links. See Razorpay’s [Payment Link test guide](https://razorpay.com/docs/payments/payment-links/create/?preferred-country=IN) and [Standard Payment Link API](https://razorpay.com/docs/api/payments/payment-links/create-standard/?preferred-country=IN).

Create a local `.env` (never commit it):

```env
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_separate_webhook_secret

REBOUND_EXECUTION_MODE=test_mode
REBOUND_ENABLE_LLM_PROPOSER=false
DATABASE_URL=sqlite:///./rebound.db
POLICY_VERSION=mvp-v1
APP_URL=http://localhost:5173
API_URL=http://localhost:8000
```

Then seed a fresh batch, open a case whose gated proposal is `payment_link`, and execute that one case. Rebound will create a standard test Payment Link with notifications and reminders disabled; it will return the test link ID and URL. Avoid bulk test-mode execution.

For a genuine webhook check, configure `POST /api/v1/ingest/webhooks/razorpay` on a public HTTPS staging URL or a supported local tunnel, set the same **webhook secret** in Razorpay and `.env`, and subscribe to the Payment Link event you are testing. Razorpay cannot deliver webhooks to `localhost`; it requires a public URL and signs the raw body with `X-Razorpay-Signature`. Follow the [official validation and test guide](https://razorpay.com/docs/webhooks/validate-test/?preferred-country=IN).

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
| Technical design | [architecture index](architecture/README.md) — decomposition, scope, system overview, data model, ADRs, and API surface |
| Evidence | [benchmark index](evidence/benchmarks/README.md) · [sensitivity notes](evidence/benchmarks/sensitivity.md) · [research-evidence guide](evidence/research/README.md) |
| Build history | [build journal](BUILD_LOG.md) · [day-by-day build log](docs/build-log/README.md) · [documentation system](docs/DOCUMENTATION_SYSTEM.md) |
| Operations and supporting material | [external requirements](docs/EXTERNAL_REQUIREMENTS.md) · [schedule](SCHEDULE.md) · [publish history](docs/WORKER_PUSH_PLAN.md) · [Medium draft](docs/medium-drafts/00-intro-and-series-plan.md) |

## Author

**Mukul Prasad** · CSE, M.S. Ramaiah Institute of Technology, Bengaluru

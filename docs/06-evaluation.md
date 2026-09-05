# 06 — Evaluation

> The product is judged on decision quality and safety—not a vanity total of “recovered” value.

## Measurement contract

`simulated_net_value_delta` = `net_value(Rebound) - net_value(Baseline A)`.

The evaluator runs Rebound, Baseline A, and Baseline B on the same seeded synthetic portfolio. Recovery outcomes are probabilistic simulations; the metric is not live merchant revenue, production ROI, or a statistically independent merchant hold-out result.

Full reproduction details: [`evidence/benchmarks/README.md`](../evidence/benchmarks/README.md). Baseline policy definitions: [`research/15-baseline-policies-draft.md`](../research/15-baseline-policies-draft.md).

## Current evidence

| Goal | Evidence | Current status |
| --- | --- | --- |
| Safe recovery loop | Ingest → propose → deterministic gate → execute → audit is covered by the backend suite. | Met locally |
| Regression confidence | `cd src && python -m pytest tests -q` returned **37 passed** on 5 Sep 2026. | Met locally |
| Decision comparison | Eval reports Baseline A, Baseline B, and Rebound with a paired simulated net-value delta. | Met on synthetic data |
| Real Razorpay side effect | Executor creates a guarded Test Mode link, preserves a pending outcome, and can refresh it through Razorpay's authenticated read API. | Implementation ready; account proof pending |
| Full external outcome loop | One Test Mode Payment Link payment plus signed public webhook delivery (or authenticated status refresh). | Pending account proof |
| Merchant-generalizable uplift | Independent hold-out data and consented production observation. | Not claimed |

## Failure modes covered

| Scenario | Expected result |
| --- | --- |
| Empty evaluation batch | Clear `no_cases` error |
| Negative expected value | Gate rewrites to `stop` |
| Low confidence | Gate rewrites to `stop` |
| High value, low confidence | Gate rewrites to `escalate` |
| Retry cap reached | Gate rewrites to `stop` |
| Optional LLM unavailable or malformed | Local EV proposer is used; no action can bypass policy |
| MVP-mode keys absent or live | Payment Link remains dry-run or is rejected before an external call |

## Evidence boundary

The next highest-value demo artifact is not another synthetic chart. It is a single controlled MVP-mode Payment Link and signed webhook capture, labelled **mvp_mode**, followed by the existing synthetic evaluation story. The operating procedure is in [`README.md`](../README.md#mvp-mode-functional-testing-without-production-money).

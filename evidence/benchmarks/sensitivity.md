# Sensitivity notes

Lift on synthetic sims depends on RNG seed and batch composition.

## Practice

1. Run `run_eval` with seeds `42`, `43`, `44`.
2. Record `lift_value`, Rebound/Baseline A `net_value`, and `simulated_share`.
3. If sign flips, say so in the demo — honesty > cherry-pick.

## Interpretation

- Positive lift: Rebound’s EV picks beat fixed ladder **under this sim**.
- Near-zero / negative: still valid product story if stop-rate / cost savings improve (inspect `intervention_cost` and `stop_rate`).

Primary comparator remains **Baseline A** (fixed ladder). Baseline B is a second heuristic foil.

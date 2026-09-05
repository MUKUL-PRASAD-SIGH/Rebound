# Baseline policies (locked for MVP eval)

> Refined Day 02. Used by `eval` module.

## North-star

```text
lift_value = net_value(Rebound) - net_value(Baseline A)

net_value = recovered_value - intervention_cost
```

Report also: recovery_rate, stop_rate, escalation_rate, simulated_share.

## Cost table (demo units)

| Action | Cost (paise-equivalent demo units) |
| --- | --- |
| `silent_retry` | 50 |
| `payment_link` | 200 |
| `notify_update_method` | 300 |
| `escalate` | 100 |
| `stop` | 0 |

Tune in config; keep constant across Rebound and baselines in a run.

## Baseline A — Fixed ladder (primary)

Parameters: `N_RETRY=2`

```text
if attempt_n < N_RETRY:
    action = silent_retry
elif not sent_update_link:
    action = payment_link   # or notify_update_method if links disabled
else:
    action = stop
```

No EV. No skip of low-value cases.

## Baseline B — Always aggressive (stretch)

Prefer `notify_update_method` then `payment_link` until hard caps (`max_actions=5`), never voluntary early stop unless exhausted.

## Rebound policy

1. Compute EV for each allowlisted action using scorer outputs.  
2. Drop actions failing hard caps (retry/notify counts).  
3. Pick max-EV action with `ev >= min_ev` and `confidence >= min_confidence`.  
4. Else `stop`. High-value + low-confidence → `escalate` if configured.  

### Default thresholds (starting point)

| Knob | Default |
| --- | --- |
| `min_ev` | 0 |
| `min_confidence` | 0.35 |
| `max_silent_retries` | 3 |
| `max_notifies` | 2 |
| `escalate_if_value_paise_ge` | 500000 (₹5000) and confidence < 0.5 |

## Recovery labeling

| Source | Label |
| --- | --- |
| Payment Link paid in MVP mode (Razorpay Test Mode) | `mvp_mode` recovered |
| Synthetic outcome model / scripted resolve | `simulated` recovered |
| Stop without recovery | not recovered |

Synthetic generator must document how “true recovery” labels are assigned so eval is reproducible.

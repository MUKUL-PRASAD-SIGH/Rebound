# Baseline policies (draft for Aug 22 architecture)

> Enough to lock evaluation intent on Aug 21. Flesh out thresholds tomorrow.

## North-star

**Incremental recovered value** on a held-out batch:

`lift = value_recovered(Rebound) - value_recovered(baseline_policy)`

Also report: recovery rate, actions taken, stops, escalations, estimated intervention cost.

## Baseline A — Fixed ladder (primary)

1. On failure → silent retry up to N times (fixed schedule)  
2. Then → always issue payment-method update / payment link  
3. Then → stop  

No EV. No “skip low-value.” No channel choice.

## Baseline B — Always aggressive (stress)

Always take the richest allowed outreach/action until hard caps.  
Shows whether Rebound’s **stops** reduce wasted cost.

## Rebound policy sketch

For each case compute approx:

`EV(action) = P(recover | action, x) * value(x) - cost(action, x)`

Pick allowlisted action with best EV if:

- above confidence / EV threshold  
- under retry + communication + discount caps  
- else **stop** or **escalate**

## Honest labels

| Outcome type | Label in reports |
| --- | --- |
| Test-mode payment success | recovered (test-mode) |
| Simulated outreach → assumed convert | simulated (clearly marked) |
| Stop with no action | correct stop / missed opportunity (analyze both) |

# Video script (~2–3 min)

> Record after the Sep 3 tested rehearsal; include the verified package in the Sep 4 submission. Never describe simulated recovery or lift as live merchant revenue.

1. **Hook — 15s**
   - “Failed payments leak revenue, but more retries are not always the answer.”
   - Show the Rebound overview and the at-risk queue.
2. **Thesis — 20s**
   - “Rebound is an expected-value decision layer above recovery rails.”
   - “It decides whether, which action, and when to act — including when to stop.”
3. **Policy differentiation — 25s**
   - Open one case and call out the expected value, confidence, and gate outcome.
   - “The model proposes; deterministic policy limits decide whether an action is allowed, stopped, or escalated.”
4. **Demo — 75–90s**
   - Seed the 60-case sample batch.
   - Run Eval before batch execution; show Rebound beside Baseline A and Baseline B.
   - Say: “This is simulated net-value delta, not live revenue.”
   - Decide and execute one case, then show its append-only audit trail.
   - Finish on the global audit view.
5. **Close — 15s**
   - “Rebound gives merchant teams a safer recovery controller: measurable, policy-gated, and fully auditable.”

## Recording checklist

- Use a clean sample batch and default evaluation seed 42
- Keep the API and web terminals out of the recording frame
- Capture the Overview, case decision, Eval, and Audit views in that order
- Use only the verified numbers from the Sep 3 rehearsal

# Demo recording script (2–3 minutes)

Use this as the exact screen-and-voice plan for the Buildathon recording. The story is simple: **Rebound decides whether recovery is worth attempting, applies deterministic guardrails, and makes every result auditable.**

## Before you record

1. Start the API and web app, then open `http://127.0.0.1:5173`.
2. Use a fresh local sample batch. The recording flow assumes the default evaluation seed, `42`.
3. Keep terminals, `.env`, API keys, and browser tabs with personal information out of frame.
4. Record at normal browser zoom with the app window large enough to read the queue, evaluation labels, and audit events.
5. Run **Evaluation before Batch decide+execute**. Batch execution changes the open queue, so an evaluation after it is not the clean headline comparison.

## What to show and say

| Time | Show / click | Say |
| --- | --- | --- |
| 0:00–0:15 | **Overview** page. Keep the Recovery command center and its status card in view. | “Failed payments leak revenue, but more retries are not always the answer. Rebound is a recovery decision controller for payment failures.” |
| 0:15–0:30 | Stay on Overview; point to the decision-path card. | “Instead of blindly retrying, Rebound estimates recovery value, proposes a bounded action, applies deterministic policy rules, and records the result.” |
| 0:30–0:45 | Click **Seed batch**. When it completes, point to the Recovery queue metric. | “I’m loading the repeatable 60-case synthetic portfolio. This gives every policy the same starting batch.” |
| 0:45–1:15 | Click **View evaluation**, then **Run fresh evaluation**. Show the three policy cards and the `SIMULATED OUTPUT` badge. | “First I compare Rebound with Baseline A, a fixed recovery ladder, and Baseline B, an alternate heuristic. The headline is simulated net-value delta versus Baseline A—not live merchant revenue.” |
| 1:15–1:30 | Point to Rebound’s recovery, cost, and stop-rate values. | “This is the key distinction: Rebound can spend when the expected value is positive, but it can also stop when recovery is not worth the cost.” |
| 1:30–1:55 | Click **Recovery queue** and open one case. Click **Preview decision** first. Show proposed action, gated action, expected value, confidence, and reason. | “For an individual failed payment, the model proposes an action, but it has no authority by itself. The deterministic policy gate can allow it, stop it, or escalate it for a human.” |
| 1:55–2:15 | Click **Decide & execute** on that same case. Show the result and the case audit table. | “When an action is allowed, execution stays test-mode-safe. The system writes the decision, gate result, execution attempt, and outcome to an append-only audit trail.” |
| 2:15–2:35 | Click **Audit trail**. Scroll only enough to show multiple event types across cases. | “This global view gives an operator evidence for every recovery decision across the portfolio—not just a black-box score.” |
| 2:35–2:50 | Return to Overview or stay on Audit trail for the close. | “Rebound sits above payment recovery rails. It decides whether, which action, and when—including when to stop—so recovery can be measurable, policy-gated, and auditable.” |

## One optional ops view

Only after the evaluation segment, return to **Overview** and click **Run queue** if you want to show portfolio-scale execution. Say: “The same policy-gated loop can process every open case.” Do **not** use an evaluation after this step as the headline unless you start again with a fresh batch.

## Words to use—and avoid

Use these exact phrases:

- “Expected-value decision layer above Razorpay recovery rails.”
- “The model proposes; deterministic policy gates decide.”
- “Simulated net-value delta versus Baseline A.”
- “Test-mode-safe execution and append-only audit trail.”

Never say:

- “We recovered this live revenue.”
- “This is merchant ROI.”
- “The model autonomously moves money.”

## Final recording checklist

- [ ] Overview, Evaluation, one Case workspace, and Audit trail are all visible in the final cut.
- [ ] The evaluation label `simulated_net_value_delta` or `SIMULATED OUTPUT` is shown.
- [ ] Rebound, Baseline A, and Baseline B are all visible together.
- [ ] One case shows expected value, confidence, a gate result, and audit events.
- [ ] No terminal, key, webhook secret, or personal data is visible.
- [ ] The final sentence explains that Rebound includes a **stop** decision.

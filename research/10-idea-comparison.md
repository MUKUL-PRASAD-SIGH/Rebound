# 10 — Idea / Track Comparison

> Scoring is my reasoned judgment after first-pass research (21 Aug 2026), not a scientific instrument.  
> Scale: 1 (weak) – 5 (strong). Subjective but explicit.

## Comparison matrix

| Factor | T01 Agentic Commerce | T02 Risk | T03 Revenue Recovery | T04 Finance Controller | T05 Open |
| --- | --- | --- | --- | --- | --- |
| Problem severity | 5 | 5 | 5 | 4 | ? |
| Market relevance now | 5 | 5 | 5 | 4 | ? |
| Razorpay strategic relevance | 5 | 5 | 5 | 4 | ? |
| Current Razorpay overlap (higher = more collision) | 5 | 5 | 4 | 4 | ? |
| Room above existing stack | 3 | 2 | **4** | 3 | ? |
| Technical novelty (student-feasible) | 3 | 3 | **4** | 3 | ? |
| AI depth | 4 | **5** | **5** | 3 | ? |
| Agentic depth | **5** | 3 | **5** | 3 | ? |
| Data availability (honest) | 3 | **2** | **4** (synthetic + test-mode) | **5** (synthetic) | ? |
| API / test-mode feasibility | 3 | 2 | **4** | 4 | ? |
| ₹0 feasibility | 3 | 3 | **4** | **5** | ? |
| Evaluation clarity | 3 | **5** | **4** | **5** | 2 |
| Measurable business impact story | 4 | 4 | **5** | 3 | ? |
| Demo potential | **5** | 3 | 4 | 3 | ? |
| Production-oriented potential | 3 | 3 | **4** | 4 | ? |
| Reliability / safety burden | 5 (high burden) | 5 | 4 | 3 | ? |
| Differentiation if executed well | 3 | 2 | **4** | 3 | ? |
| Judging potential | 4 | 3 | **5** | 3 | 3 |
| Hiring / internship signal | 4 | 4 | **5** | 3 | 3 |
| Fit with my skills | 4 | **5** | **5** | 3 | 3 |
| Risk of becoming generic | **4** (high risk) | **5** | 3 | 4 | 5 |

## Trade-off notes

### Track 01
Highest narrative heat. Highest chance of looking like Razorpay's own agentic demos. Only works with a merchant-side gap thesis.

### Track 02
Best pure ML flex. Worst honest-data story. Collides with Vulcan/SHIELD/Bumblebee/Dispute agents.

### Track 03
Best blend of AI depth, measurable ₹ story, agent loop, and my stack — **after** rejecting naive retries. Still collides with Agent Studio + Intelligent Retry unless framed as EV decision layer.

### Track 04
Cleanest scoreboard. Easiest to underwhelm. Backup lane.

### Track 05
Only if something beats the above. Currently no.

## Production-vs-hackathon stress test (shortlist)

Question: *If presented to a Razorpay engineer, does the architecture still make sense?*

| Candidate | Reliability story | Idempotency | Guardrails | Evaluation | Engineer smell test |
| --- | --- | --- | --- | --- | --- |
| Chat checkout clone | Weak unless Reserve-Pay-like bounds | Easy to get wrong | Often missing | Vanity conversion | Fail |
| Generic fraud classifier | N/A | N/A | Thresholds only | ROC without FP cost | Fail |
| EV recovery controller | Strong if policy engine is real | Must design for webhooks | Central | Baseline vs treatment | Pass (if built) |
| Exception-first reconciler | Strong | Matching keys | HITL | Match/exception rates | Pass (if non-trivial) |

## Provisional ranking after research

1. **Track 03 — decision-intelligence revenue recovery** (conditional)
2. **Track 01 — merchant agent-readiness / bounded growth agent** (conditional)
3. Track 04 — backup
4. Track 02 — parked
5. Track 05 — unused

## What would change this ranking

- If test-mode cannot support the recovery loop cleanly → raise Track 04 / narrowed Track 01
- If I find a defensible risk dataset + niche → reconsider Track 02
- If Agent Studio already covers my exact Track 03 thesis in public docs → narrow further or switch

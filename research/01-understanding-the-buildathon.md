# 01 — Understanding the Buildathon

Source of truth for tracks: [razorpay.com/buildathon/](https://razorpay.com/buildathon/) (read 21 Aug 2026).

## What this is (and is not)

This is **not** a weekend vanity hackathon pitch contest.

It is a hiring filter disguised as a build challenge:

- Students only
- Build something real on a chosen track
- Show: public repo, ~5 min pitch video, architecture
- Signal → panel → possible AI Builder Internship (₹75k/month, 6 or 12 months, Bangalore from September)

That changes how I evaluate ideas. A flashy demo that collapses under one failure case is weak signal. A smaller system with measured outcomes, bounded actions, and an audit trail is stronger signal.

## The five tracks (verbatim intent, my paraphrase)

| Track | Official ask (compressed) | The bar that matters |
| --- | --- | --- |
| **01 — AI Growth & Agentic Commerce** | Grow merchant revenue **or** make a merchant transactable by an AI buyer end-to-end on test-mode APIs | Every money action explainable, bounded, gated; audit trail; one failure handled gracefully |
| **02 — AI Risk Manager** | Detector / verifier / auto-responder for one class of loss; measured precision & recall on held-out set | Honest metrics incl. false-positive cost; **defense-only** |
| **03 — AI Revenue Recovery** | Detect revenue at risk → choose intervention → execute bounded recovery | Measured money recovered across a batch; escalation; stopping rules; audit trail |
| **04 — AI Finance Controller** | Close one finance-ops loop on 50+ synthetic records; report match rate + unresolved exceptions | Throughput + accuracy + honest exception list |
| **05 — Open Track** | Build what you believe should exist | Same execution bar; open ≠ easier |

## How I am reading the tracks

They are five competing **hypotheses**, not five equally good homework prompts.

My first-pass instinct ranking (before deep product research):

1. Track 03 — sounds closest to decision intelligence + measurable ₹
2. Track 01 — strategically hot, but maybe too close to Razorpay's own demos
3. Track 02 — strong ML fit for me, but data + false-positive cost are brutal
4. Track 04 — clear evaluation rubric, risk of "polished dashboard"
5. Track 05 — only if a defined track is weaker after research

**This ranking is provisional.** Research already moved pieces around — see later files.

## Judging / hiring signal (my reading)

What I think a Razorpay engineer would care about more than buzzwords:

- Did you integrate real Razorpay surfaces (even test-mode)?
- Did you measure something non-vanity?
- Did you handle failure, duplicates, timeouts, malformed model output?
- Did you put guardrails between the model and money?
- Did you avoid recreating a product Razorpay already ships?

## Open questions about the program itself

- [ ] Exact submission deadline / format beyond the public page (TODO: confirm on portal)
- [ ] Whether Agent Studio / Intelligent Retry / Vulcan are in-scope to *compose with* or off-limits to *recreate* (my working assumption: compose above; do not recreate)
- [ ] Test-mode coverage for subscriptions, webhooks, payment links, invoices (TODO: verify against docs with keys)

## Next

Read each track as a research problem. For every track: existing Razorpay stack → gap → feasibility → reject or shortlist.

# Demo runbook (local)

> **Release cadence:** finish the project build by Sep 2, rehearse and test this full flow on Sep 3, then submit on Sep 4.

## Fast start (Make)

From the repository root, use two terminals:

```bash
# terminal 1
make api

# terminal 2
make web
```

Useful checks:

```bash
make test
make seed
make eval
```

> Make is optional on Windows. Use the direct commands below from PowerShell if GNU Make is unavailable.

## Start manually

```bash
# terminal 1 — API
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000

# terminal 2 — web
cd src/apps/web && npm install && npm run dev
```

Open http://127.0.0.1:5173. The web app proxies `/api` to the API on port 8000.

## Happy path (2–3 min)

**Order matters:** run **Eval before** heavy batch decide so `lift_value` is measured on a clean case batch (default seed **42**).

1. Home → **Seed sample batch** (60 cases). Use a fresh database before each Sep 3 rehearsal.
2. Eval → **Run eval** → show `lift_value` + label `simulated_net_value_delta` (simulated, not live ₹).
3. Cases → open one → **Decide** / **Decide+execute** → show gate + audit + outcome.
4. Optional: Home → **Batch decide+execute open** (ops demo; do not re-run eval as the headline after this unless you re-seed).
5. Audit → cross-case trail.

## Say out loud

- “Expected-value decision layer above Razorpay recovery rails.”
- “We decide whether / which / when — including stop.”
- “Lift is simulated net delta vs Baseline A — not live ₹.”
- “Default demo seed is 42; recoveries are probabilistic sims.”

## Sep 3 rehearsal exit criteria

- `cd src && python -m pytest tests -q` passes
- `cd src/apps/web && npm run build` passes
- Health → seed → eval → decide/execute → audit works in one browser session
- The spoken demo uses “simulated net delta,” never live revenue or merchant ROI

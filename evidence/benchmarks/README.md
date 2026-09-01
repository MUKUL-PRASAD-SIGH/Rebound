# Benchmarks (synthetic)

## Claim framing

`lift_value` = net(Rebound) − net(Baseline A), labeled **`simulated_net_value_delta`**.

Recoveries are drawn from scored probabilities. **Not real merchant rupees.** Do not present as production ROI.

## Reproduce

```bash
# from repo root
pip install -r requirements.txt
python src/scripts/generate_batch.py
python src/scripts/train_model.py

# API
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000

# seed + eval (separate shell)
curl -X POST http://127.0.0.1:8000/api/v1/ingest/synthetic
python src/scripts/run_eval.py
# or: python src/scripts/run_eval.py --api
```

## Corpus

- Default batch: `src/scripts/sample_batch.json` (≥50 synthetic cases)
- Model: `src/scripts/recover_model.json`

## Edge cases to check

| Case | Expected |
| --- | --- |
| Empty DB eval | HTTP 400 `no_cases` |
| Negative EV action | Policy rewrite → stop (`ev_below_min`) |
| Low confidence | Rewrite → stop |
| High value + low confidence | Rewrite → escalate |
| Max silent retries | Rewrite → stop |
| Stop action | Not counted as recovery |

## Artifacts

Paste latest JSON aggregates under `evidence/benchmarks/runs/` when recording a judge demo (optional; gitignore large dumps if needed).

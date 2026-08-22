# Day 03 — 23 Aug 2026

## Goal
Skeleton: backend + DB + API routes + frontend shell so the repo runs with empty paths wired.

## What I did
- Python package `src/rebound/*` (config, db models, schemas, module stubs: ingest/features/scoring/propose/policy/execute/audit/eval)
- FastAPI app `src/apps/api/main.py`
  - Live: `GET /health`, `GET /metrics/summary`, `GET /cases`, `GET /cases/{id}`, `GET /cases/{id}/audit`, `POST /ingest/synthetic`
  - Stubs (intentional): decide, execute, eval, webhook ingest
- SQLite + SQLAlchemy models per `architecture/data-model.md`
- Policy allowlist gate stub; audit append helper
- Sample batch (`src/scripts/sample_batch.json`) + `seed_batch.py`
- React/Vite ops UI: Home, Cases, Case detail, Eval, Audit placeholders
- `requirements.txt`, `src/apps/web/package.json`, `src/README.md`
- Root README “How to run (Day 03 skeleton)”

## Decisions
- Run API with `--app-dir src` (`apps.api.main:app`, imports `rebound.*`)
- Vite proxies `/api` → backend `:8000`
- Synthetic ingest works today; decide/execute remain stubs until later days
- Commit style for this day: `feat: Day 03 skeleton — …`

## Problems
- Port 8000 sometimes occupied locally → verified on `:8001` during smoke test (same app)

## Experiments
- Smoke test: health → synthetic ingest (5 cases) → metrics (`cases_total=5`) → list cases

## Evidence
- Code: `src/` tree (commit `70162c4`)
- Docs: this file + `BUILD_LOG.md` Day 03 section
- Local verification notes above

## Done for Day 03
- [x] API boots with health route  
- [x] DB models created on startup  
- [x] Synthetic seed path works  
- [x] Cases listable via API  
- [x] React shell pages exist  
- [x] Run instructions in README  
- [x] Day log + BUILD_LOG updated  
- [x] Pushed to `origin/main`  

## Stop line
**Day 03 ends here.** No decide/execute/eval implementation in this day.

## Next (only when starting Day 04)
- Happy-path: rules ladder decide → dry_run execute → audit in UI

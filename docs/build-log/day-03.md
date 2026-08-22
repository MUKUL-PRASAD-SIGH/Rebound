# Day 03 — 23 Aug 2026

## Goal
Skeleton: backend + DB + API routes + frontend shell so the repo runs with empty paths wired.

## What I did
- Python package `src/rebound/*` (config, db models, schemas, module stubs)
- FastAPI app `src/apps/api/main.py` — health, metrics, cases, audit, synthetic ingest, stubs for decide/execute/eval/webhook
- SQLite + SQLAlchemy models per architecture data model
- Policy allowlist gate stub; audit append helper
- Sample batch + `seed_batch.py`
- React/Vite ops UI: Home, Cases, Case detail, Eval, Audit placeholders
- `requirements.txt` + web `package.json`

## Decisions
- `--app-dir src` so imports are `apps.api.main` / `rebound.*`
- Vite proxies `/api` → `:8000`
- Synthetic ingest works today; decide/execute remain stubs until Day 04–05

## Problems
- None blocking

## Experiments
- Verified API health + synthetic seed against local uvicorn

## Evidence
- `src/` tree
- Local: `GET /api/v1/health`, `POST /api/v1/ingest/synthetic`

## Tomorrow (Aug 24 — Core workflow)
- Happy-path case loop without ML: ingest → list → decide stub→real rules ladder → execute dry_run → audit visible in UI

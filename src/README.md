# Source

| Path | Role |
| --- | --- |
| `apps/api` | FastAPI entry (`apps.api.main:app`) |
| `apps/web` | React ops UI |
| `rebound/` | Domain packages |
| `scripts/` | Seed / eval helpers |

```bash
# API (from repo root)
python -m pip install -r requirements.txt
python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000

# Web
cd apps/web && npm install && npm run dev
```

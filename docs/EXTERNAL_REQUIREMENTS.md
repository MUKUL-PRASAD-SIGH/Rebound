# External tools, APIs & runtime requirements

Single checklist of everything needed to run Rebound end-to-end. **Nothing here is required for the default local demo** except Python + Node.

---

## Required (local demo)

| Tool | Why | Notes |
| --- | --- | --- |
| **Python 3.10+** | API, scoring, eval, scripts | `pip install -r requirements.txt` |
| **Node.js 18+ / npm** | React ops UI (Vite) | `cd src/apps/web && npm install` |
| **Git** | Repo / commits | Already in use |

### Python packages (from `requirements.txt`)

| Package | Role |
| --- | --- |
| `fastapi`, `uvicorn` | HTTP API |
| `sqlalchemy` | SQLite ORM |
| `pydantic`, `pydantic-settings` | Config + schemas |
| `python-dotenv` | Load `.env` |
| `numpy`, `scikit-learn` | Features + recoverability model |
| `httpx` | FastAPI `TestClient` / optional future Razorpay HTTP | **Required for pytest**; not used in dry_run execute path |
| `pytest` | Test suite | `cd src && python -m pytest tests -q` |

### Default ports

| Service | URL |
| --- | --- |
| API | http://127.0.0.1:8000 |
| Web | http://127.0.0.1:5173 (proxies `/api` → 8000) |

---

## Optional — Razorpay (test mode)

| Env var | Used for | Required? |
| --- | --- | --- |
| `RAZORPAY_KEY_ID` | Future Payment Link create | **No** — dry_run works without keys |
| `RAZORPAY_KEY_SECRET` | Future Payment Link create | **No** |
| `RAZORPAY_WEBHOOK_SECRET` | Signature verify (stubbed) | **No** — ingest validates payload shape only |
| `REBOUND_EXECUTION_MODE` | `dry_run` (default) \| `test_mode` | Defaults to `dry_run` |

**Current behavior:** even with keys present, Payment Link HTTP is still deferred to a safe dry_run placeholder so demos never invent live ₹. Real SDK wiring is optional polish, not a blocker.

Copy [`.env.example`](../.env.example) → `.env` only if you want to experiment with keys.

---

## Optional — LLM proposer

| Env var | Used for | Required? |
| --- | --- | --- |
| `REBOUND_ENABLE_LLM_PROPOSER=true` | Flag on proposer path | **No** — default EV model |
| `OPENAI_API_KEY` / `ANTHROPIC_*` / `GOOGLE_*` / `GROQ_*` | Listed in `.env.example` for future use | **Not wired** — flag currently passthroughs EV pick with a tagged rationale |

Product thesis does **not** depend on an LLM.

---

## Optional — developer convenience

| Tool | Why |
| --- | --- |
| `make` (GNU Make / or run listed targets manually on Windows) | `api`, `web`, `generate`, `train`, `eval`, `test` |
| `curl` | Seed / health without UI |
| Browser | Ops console at :5173 |

---

## Not required

- LangGraph / CrewAI / Docker / cloud GPU  
- Live Razorpay production keys  
- Paid LLM API for core decide → gate → execute → eval loop  
- Internet (after deps installed) — full demo is offline synthetic

---

## Verify install

```bash
python -m pip install -r requirements.txt
python src/scripts/generate_batch.py
python src/scripts/train_model.py
cd src && python -m pytest tests -q

python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000
# other terminal:
cd src/apps/web && npm install && npm run dev
```

Demo path (local until Day 06 push): [`docs/submission/demo-runbook.md`](submission/demo-runbook.md)

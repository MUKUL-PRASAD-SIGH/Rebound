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
| `httpx` | FastAPI `TestClient` / Razorpay test-mode HTTP | **Required for pytest**; only calls Razorpay when test mode and both keys are configured |
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
| `RAZORPAY_KEY_ID` | Payment Link Basic Auth key | **No** — dry_run works without keys |
| `RAZORPAY_KEY_SECRET` | Payment Link Basic Auth secret | **No** — both key and secret are required for a test-mode call |
| `RAZORPAY_WEBHOOK_SECRET` | Webhook signature verification | **No** — when set, validates `X-Razorpay-Signature` against the raw request body |
| `REBOUND_EXECUTION_MODE` | `dry_run` (default) \| `test_mode` | `test_mode` plus both test keys is required to create a real Razorpay **test-mode** Payment Link; a key ID not starting `rzp_test_` is rejected before any HTTP call |

**Execution safety:** the default remains offline `dry_run`. In explicitly configured `test_mode`, Rebound creates one standard Payment Link per decision with notifications/reminders disabled, a deterministic 40-character-or-less `reference_id`, and reconciliation by that reference after an ambiguous request failure. Outcomes remain labelled `simulated`; creating a link is not treated as a recovered payment.

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

Demo path and Sep 3 rehearsal guide: [`docs/submission/demo-runbook.md`](submission/demo-runbook.md)

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
| `httpx` | FastAPI `TestClient` / Razorpay MVP-mode HTTP | **Required for pytest**; only calls Razorpay when MVP mode and both keys are configured |
| `pytest` | Test suite | `cd src && python -m pytest tests -q` |

### Default ports

| Service | URL |
| --- | --- |
| API | http://127.0.0.1:8000 |
| Web | http://127.0.0.1:5173 (proxies `/api` → 8000) |

---

## Optional — Razorpay MVP mode (backed by Razorpay Test Mode)

| Env var | Used for | Required? |
| --- | --- | --- |
| `RAZORPAY_KEY_ID` | Payment Link Basic Auth key | **No** — dry_run works without keys |
| `RAZORPAY_KEY_SECRET` | Payment Link Basic Auth secret | **No** — both key and secret are required for an MVP-mode call |
| `RAZORPAY_WEBHOOK_SECRET` | Webhook signature verification | **No** — required only for signed public webhook testing; validates `X-Razorpay-Signature` against the raw request body |
| `REBOUND_EXECUTION_MODE` | `dry_run` (default) \| `mvp_mode` | `mvp_mode` plus both Razorpay Test Mode keys creates a real Razorpay Test Mode Payment Link; a key ID not starting `rzp_test_` is rejected before any HTTP call |

**Execution safety:** the default remains offline `dry_run`. In explicitly configured `mvp_mode`, Rebound creates one standard Payment Link per decision with notifications/reminders disabled, a deterministic 40-character-or-less `reference_id`, and reconciliation by that reference after an ambiguous request failure. It records the link as **pending** and accepts recovery only after a signed `payment_link.paid` webhook. Other recovery outcomes remain labelled `simulated`.

MVP mode additionally allows authenticated, read-only Test Mode inspection:

- `POST /api/v1/cases/{case_id}/refresh-payment-link` reconciles a Rebound-created link from Razorpay’s current `paid` / `expired` / `cancelled` status when a public webhook is not available.
- `GET /api/v1/razorpay/subscriptions/{sub_id}` fetches one subscription.
- `GET /api/v1/razorpay/subscriptions/{sub_id}/invoices` fetches its invoices.

All three require `mvp_mode` and Test Mode credentials. They reject live keys and have no create, capture, cancel, or update capability.

Copy [`.env.example`](../.env.example) → `.env` only if you want to experiment with keys.

---

## Optional — LLM proposer

| Env var | Used for | Required? |
| --- | --- | --- |
| `REBOUND_ENABLE_LLM_PROPOSER=true` | Enables the OpenAI structured-output proposer | **No** — the default EV model remains the offline proposer |
| `OPENAI_API_KEY` | Server-side key for the optional OpenAI request | Required only when the flag is `true`; never expose it in the web app or commit it |
| `OPENAI_MODEL` | Optional OpenAI model override | Defaults to `gpt-4o-mini` |

When enabled, Rebound sends only non-identifying recovery signals (amount, currency, failure class, attempt count, tenure, payment method, and deterministic candidate metrics) to the OpenAI Responses API. The model can choose only from precomputed, non-exhausted action candidates and returns schema-constrained JSON. Rebound recomputes probability and expected value deterministically, then sends the proposal through the same mandatory policy gate. Missing credentials, failed requests, and invalid model output fall back to the offline EV proposer. Requests use `store=false`.

Product thesis does **not** depend on an LLM; the default decide → gate → execute → eval loop remains offline. To use it in MVP mode, enable the flag and provide an `OPENAI_API_KEY`; it still has no execution authority.

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

Local run, MVP-mode keys, demo flow, and verification directions: [`README.md`](../README.md#mvp-mode-functional-testing-without-production-money)

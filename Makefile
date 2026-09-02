.PHONY: api web seed train eval test generate

api:
	python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000

web:
	cd src/apps/web && npm run dev

generate:
	python src/scripts/generate_batch.py

train:
	python src/scripts/train_model.py

seed:
	curl -X POST http://127.0.0.1:8000/api/v1/ingest/synthetic

eval:
	python src/scripts/run_eval.py

test:
	cd src && python -m pytest tests -q

#!/usr/bin/env python3
"""Run Baseline A vs Rebound eval (API or in-process)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def via_api(base: str = "http://127.0.0.1:8000", seed: int = 42) -> None:
    req = urllib.request.Request(
        f"{base}/api/v1/eval/runs?seed={seed}", method="POST", data=b"{}"
    )
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        print(resp.read().decode())


def via_local(seed: int = 42) -> None:
    from rebound.db.session import SessionLocal, init_db
    from rebound.eval import run_eval

    init_db()
    db = SessionLocal()
    try:
        print(json.dumps(run_eval(db, seed=seed), indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.api:
        via_api(seed=args.seed)
    else:
        via_local(seed=args.seed)

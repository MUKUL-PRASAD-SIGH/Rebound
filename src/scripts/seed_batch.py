#!/usr/bin/env python3
"""Seed synthetic cases via the running API (or print curl hint)."""

from __future__ import annotations

import sys
import urllib.error
import urllib.request

API = "http://127.0.0.1:8000/api/v1/ingest/synthetic"


def main() -> int:
    try:
        req = urllib.request.Request(API, method="POST", data=b"")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(resp.read().decode("utf-8"))
        return 0
    except urllib.error.URLError as exc:
        print(
            "API not reachable. Start it first:\n"
            "  cd repo root\n"
            "  python -m uvicorn apps.api.main:app --app-dir src --reload --port 8000\n"
            f"Then: python src/scripts/seed_batch.py\nError: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

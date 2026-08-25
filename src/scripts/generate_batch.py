#!/usr/bin/env python3
"""Generate >=50 synthetic at-risk cases into sample_batch.json."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "sample_batch.json"
FAILURES = ["insufficient_funds", "expired_card", "bank_decline", "unknown"]
METHODS = ["upi", "card", "netbanking", "wallet"]


def main(n: int = 60, seed: int = 7) -> None:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(1, n + 1):
        fc = str(rng.choice(FAILURES))
        # ~15% high-value so escalate gate (>= 500_000) is reachable in demos
        if i <= max(3, n // 7) or rng.random() < 0.12:
            amount = int(rng.integers(500_000, 1_200_000))
        else:
            amount = int(rng.integers(4_900, 499_900))
        rows.append(
            {
                "case_key": f"syn-{i:03d}",
                "amount_paise": amount,
                "customer_ref": f"cust_{i:03d}",
                "failure_code": f"ERR_{fc.upper()}",
                "failure_class": fc,
                "attempt_n": int(rng.integers(1, 5)),
                "tenure_days": int(rng.integers(7, 400)),
                "method": str(rng.choice(METHODS)),
            }
        )
    OUT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    high = sum(1 for r in rows if r["amount_paise"] >= 500_000)
    print(f"Wrote {len(rows)} cases ({high} high-value) -> {OUT}")


if __name__ == "__main__":
    main()

"""Feature extraction + vectorization for scoring."""

from __future__ import annotations

from typing import Any

import numpy as np

from rebound.db.models import Case

FAILURE_CLASSES = [
    "insufficient_funds",
    "expired_card",
    "bank_decline",
    "unknown",
]
METHODS = ["upi", "card", "netbanking", "wallet"]


def extract_features(case: Case) -> dict[str, Any]:
    return {
        "amount_paise": case.amount_paise,
        "attempt_n": case.attempt_n,
        "tenure_days": case.tenure_days,
        "failure_class": case.failure_class,
        "method": case.method,
        "log_amount": float(np.log1p(case.amount_paise)),
    }


def vectorize(features: dict[str, Any]) -> np.ndarray:
    amount = float(features.get("amount_paise", 0))
    row = [
        float(np.log1p(amount)),
        float(features.get("attempt_n", 1)),
        float(features.get("tenure_days", 30)) / 365.0,
    ]
    fc = str(features.get("failure_class", "unknown"))
    method = str(features.get("method", "upi"))
    row.extend([1.0 if fc == c else 0.0 for c in FAILURE_CLASSES])
    row.extend([1.0 if method == m else 0.0 for m in METHODS])
    return np.asarray(row, dtype=float)

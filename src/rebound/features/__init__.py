"""Feature extraction for scoring. Logic lands Day 05."""

from __future__ import annotations

from typing import Any

from rebound.db.models import Case


def extract_features(case: Case) -> dict[str, Any]:
    return {
        "amount_paise": case.amount_paise,
        "attempt_n": case.attempt_n,
        "tenure_days": case.tenure_days,
        "failure_class": case.failure_class,
        "method": case.method,
    }

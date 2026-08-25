"""Scoring / EV helpers + lightweight sklearn recoverability model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.linear_model import LogisticRegression

from rebound.features import FAILURE_CLASSES, METHODS, vectorize
from rebound.schemas.enums import Action

# Fixed paise + rate of amount so costs compete with recover EV (not negligible).
ACTION_COST_FIXED: dict[str, int] = {
    Action.SILENT_RETRY.value: 500,
    Action.PAYMENT_LINK.value: 1_500,
    Action.NOTIFY_UPDATE_METHOD.value: 2_500,
    Action.ESCALATE.value: 800,
    Action.STOP.value: 0,
}
ACTION_COST_RATE: dict[str, float] = {
    Action.SILENT_RETRY.value: 0.02,
    Action.PAYMENT_LINK.value: 0.08,
    Action.NOTIFY_UPDATE_METHOD.value: 0.12,
    Action.ESCALATE.value: 0.04,
    Action.STOP.value: 0.0,
}

# Soft multipliers: how much of base P(recover) an action unlocks
ACTION_MULTIPLIER: dict[str, float] = {
    Action.SILENT_RETRY.value: 0.55,
    Action.PAYMENT_LINK.value: 0.70,
    Action.NOTIFY_UPDATE_METHOD.value: 0.60,
    Action.ESCALATE.value: 0.25,
    Action.STOP.value: 0.0,
}

_MODEL: LogisticRegression | None = None
_MODEL_PATH = Path(__file__).resolve().parents[2] / "scripts" / "recover_model.json"


def action_cost(action: str, value_paise: int = 0) -> int:
    fixed = ACTION_COST_FIXED.get(action, 0)
    rate = ACTION_COST_RATE.get(action, 0.0)
    return int(fixed + rate * max(0, value_paise))


def expected_value(p_recover: float, value_paise: int, action: str) -> float:
    return float(p_recover) * float(value_paise) - float(action_cost(action, value_paise))


def _heuristic_p_base(features: dict[str, Any]) -> float:
    """Fallback when model file missing."""
    p = 0.35
    fc = features.get("failure_class")
    if fc == "insufficient_funds":
        p = 0.55
    elif fc == "expired_card":
        p = 0.28
    elif fc == "bank_decline":
        p = 0.32
    attempt = int(features.get("attempt_n", 1))
    p *= max(0.35, 1.0 - 0.14 * (attempt - 1))
    if int(features.get("amount_paise", 0)) > 200_000:
        p *= 0.88
    return float(np.clip(p, 0.05, 0.85))


def action_multiplier(action: str, failure_class: str) -> float:
    base = ACTION_MULTIPLIER.get(action, 0.0)
    if failure_class == "insufficient_funds" and action == Action.SILENT_RETRY.value:
        return min(0.95, base * 1.25)
    if failure_class == "expired_card" and action == Action.NOTIFY_UPDATE_METHOD.value:
        return min(0.95, base * 1.55)
    if failure_class == "expired_card" and action == Action.SILENT_RETRY.value:
        return base * 0.55
    if failure_class == "bank_decline" and action == Action.PAYMENT_LINK.value:
        return min(0.95, base * 1.35)
    if failure_class == "unknown" and action == Action.ESCALATE.value:
        return min(0.9, base * 1.8)
    if failure_class == "unknown" and action == Action.SILENT_RETRY.value:
        return base * 0.5
    return base


def train_synthetic_model(n: int = 800, seed: int = 42) -> LogisticRegression:
    rng = np.random.default_rng(seed)
    X = []
    y = []
    for _ in range(n):
        feats = {
            "amount_paise": int(rng.integers(9900, 500000)),
            "attempt_n": int(rng.integers(1, 5)),
            "tenure_days": int(rng.integers(7, 400)),
            "failure_class": str(rng.choice(FAILURE_CLASSES)),
            "method": str(rng.choice(METHODS)),
        }
        p = _heuristic_p_base(feats)
        label = 1 if rng.random() < p else 0
        X.append(vectorize(feats))
        y.append(label)
    clf = LogisticRegression(max_iter=500)
    clf.fit(np.vstack(X), np.asarray(y))
    return clf


def save_model(clf: LogisticRegression, path: Path | None = None) -> Path:
    path = path or _MODEL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "coef": clf.coef_.tolist(),
        "intercept": clf.intercept_.tolist(),
        "classes": clf.classes_.tolist(),
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def load_model(path: Path | None = None) -> LogisticRegression | None:
    path = path or _MODEL_PATH
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        clf = LogisticRegression()
        clf.classes_ = np.asarray(payload["classes"])
        clf.coef_ = np.asarray(payload["coef"])
        clf.intercept_ = np.asarray(payload["intercept"])
        clf.n_features_in_ = clf.coef_.shape[1]
        return clf
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def get_model() -> LogisticRegression:
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    loaded = load_model()
    if loaded is None:
        loaded = train_synthetic_model()
        # Persist only under scripts/; callers may gitignore the artifact
        save_model(loaded)
    _MODEL = loaded
    return _MODEL


def reset_model_cache() -> None:
    global _MODEL
    _MODEL = None


def p_recover_base(features: dict[str, Any]) -> tuple[float, str]:
    try:
        clf = get_model()
        x = vectorize(features).reshape(1, -1)
        logit = float(clf.intercept_[0] + float(np.asarray(x.dot(clf.coef_[0].T)).reshape(-1)[0]))
        p = 1.0 / (1.0 + np.exp(-logit))
        return float(np.clip(p, 0.05, 0.95)), "model"
    except Exception:
        return _heuristic_p_base(features), "heuristic"


def score_actions(case_features: dict[str, Any], value_paise: int) -> dict[str, dict[str, Any]]:
    base, source = p_recover_base(case_features)
    fc = str(case_features.get("failure_class", "unknown"))
    out: dict[str, dict[str, Any]] = {}
    for action in ACTION_MULTIPLIER:
        mult = action_multiplier(action, fc)
        p = float(np.clip(base * mult, 0.0, 0.95))
        out[action] = {
            "p_recover": p,
            "cost": float(action_cost(action, value_paise)),
            "ev": expected_value(p, value_paise, action),
            "source": source,
        }
    return out

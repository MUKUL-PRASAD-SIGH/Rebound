#!/usr/bin/env python3
"""Train and persist recoverability logistic model."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rebound.scoring import save_model, train_synthetic_model  # noqa: E402


def main() -> None:
    clf = train_synthetic_model()
    path = save_model(clf)
    print(f"Saved model -> {path}")


if __name__ == "__main__":
    main()

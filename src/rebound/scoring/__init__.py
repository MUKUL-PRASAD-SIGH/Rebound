"""Scoring / EV helpers. Full models Day 05."""

from __future__ import annotations

from rebound.schemas.enums import Action

# Demo cost table (paise-equivalent units) — see research/15-baseline-policies-draft.md
ACTION_COSTS: dict[str, int] = {
    Action.SILENT_RETRY.value: 50,
    Action.PAYMENT_LINK.value: 200,
    Action.NOTIFY_UPDATE_METHOD.value: 300,
    Action.ESCALATE.value: 100,
    Action.STOP.value: 0,
}


def action_cost(action: str) -> int:
    return ACTION_COSTS.get(action, 0)

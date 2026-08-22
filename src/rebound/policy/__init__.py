"""Deterministic policy gate. Core logic Day 05; allowlist check ships now."""

from __future__ import annotations

from dataclasses import dataclass

from rebound.config import get_settings
from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import ALLOWLISTED_ACTIONS, Action, GateResult


@dataclass
class GateDecision:
    action: Action
    gate_result: GateResult
    reason: str
    policy_version: str


def gate(proposal: ProposalPayload) -> GateDecision:
    settings = get_settings()
    if proposal.action.value not in ALLOWLISTED_ACTIONS:
        return GateDecision(
            action=Action.STOP,
            gate_result=GateResult.REJECT,
            reason="reject_unknown_action",
            policy_version=settings.policy_version,
        )
    return GateDecision(
        action=proposal.action,
        gate_result=GateResult.ALLOW,
        reason="allowlist_pass_scaffold",
        policy_version=settings.policy_version,
    )

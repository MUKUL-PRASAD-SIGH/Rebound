"""Action proposers (rules default; LLM optional). Day 05."""

from __future__ import annotations

from rebound.schemas.api import ProposalPayload
from rebound.schemas.enums import Action


def propose_stub() -> ProposalPayload:
    return ProposalPayload(
        action=Action.STOP,
        confidence=0.0,
        p_recover=0.0,
        ev=0.0,
        rationale="proposer scaffold — implement Day 05",
    )

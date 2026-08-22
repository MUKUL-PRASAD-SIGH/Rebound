"""Razorpay + simulated executors. Day 04–05."""

from __future__ import annotations

from rebound.config import get_settings


def execution_mode() -> str:
    return get_settings().rebound_execution_mode

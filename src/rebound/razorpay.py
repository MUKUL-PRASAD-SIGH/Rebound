"""Minimal, read-safe Razorpay client for Rebound MVP mode.

Every request is guarded by the app-level MVP mode and Razorpay Test Mode key
prefix. Live credentials never reach Razorpay from this project.
"""

from __future__ import annotations

import re
from typing import Any

import httpx

from rebound.config import get_settings


RAZORPAY_API_BASE = "https://api.razorpay.com/v1"
RAZORPAY_TIMEOUT_SECONDS = 10.0
_ENTITY_ID_RE = re.compile(r"^[A-Za-z0-9_]+$")


class RazorpayMvpConfigurationError(ValueError):
    """Raised before an external call when MVP-mode configuration is unsafe."""


class RazorpayMvpRequestError(RuntimeError):
    """Raised when Razorpay Test Mode cannot fulfil a read request."""


def _mvp_auth() -> tuple[str, str]:
    settings = get_settings()
    if settings.rebound_execution_mode != "mvp_mode":
        raise RazorpayMvpConfigurationError("razorpay_reads_require_mvp_mode")
    if not settings.razorpay_key_id or not settings.razorpay_key_secret:
        raise RazorpayMvpConfigurationError("razorpay_mvp_credentials_required")
    if not settings.razorpay_key_id.startswith("rzp_test_"):
        raise RazorpayMvpConfigurationError("razorpay_mvp_mode_requires_rzp_test_key")
    return settings.razorpay_key_id, settings.razorpay_key_secret


def _entity_id(entity_id: str, *, expected_prefix: str) -> str:
    if not entity_id.startswith(expected_prefix) or not _ENTITY_ID_RE.fullmatch(entity_id):
        raise ValueError(f"invalid_{expected_prefix.rstrip('_')}_id")
    return entity_id


def _get(path: str, *, params: dict[str, str] | None = None) -> dict[str, Any]:
    try:
        response = httpx.get(
            f"{RAZORPAY_API_BASE}{path}",
            params=params,
            auth=_mvp_auth(),
            timeout=RAZORPAY_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        if isinstance(exc, RazorpayMvpConfigurationError):
            raise
        raise RazorpayMvpRequestError("razorpay_mvp_read_failed") from None
    if not isinstance(payload, dict):
        raise RazorpayMvpRequestError("razorpay_mvp_read_response_invalid")
    return payload


def fetch_payment_link(payment_link_id: str) -> dict[str, Any]:
    return _get(f"/payment_links/{_entity_id(payment_link_id, expected_prefix='plink_')}")


def fetch_subscription(subscription_id: str) -> dict[str, Any]:
    return _get(f"/subscriptions/{_entity_id(subscription_id, expected_prefix='sub_')}")


def fetch_subscription_invoices(subscription_id: str) -> dict[str, Any]:
    return _get(
        "/invoices",
        params={"subscription_id": _entity_id(subscription_id, expected_prefix="sub_")},
    )

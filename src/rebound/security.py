"""Data-minimisation helpers for Rebound's operator-facing surfaces."""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Mapping
from typing import Any


_SENSITIVE_KEYS = frozenset(
    {
        "account_number",
        "authorization",
        "bank_account",
        "card",
        "card_id",
        "card_number",
        "contact",
        "customer",
        "customer_id",
        "customer_ref",
        "cvv",
        "email",
        "ifsc",
        "notes",
        "password",
        "phone",
        "secret",
        "short_url",
        "token",
        "upi",
        "url",
        "vpa",
    }
)


def pseudonymize_customer_ref(value: str, *, salt: str = "") -> str:
    """Return a stable, non-reversible reference suitable for local storage."""
    material = value.strip().encode("utf-8")
    key = (salt or "rebound-pseudonym-v1").encode("utf-8")
    digest = hmac.new(key, material, hashlib.sha256).hexdigest()[:16]
    return f"cust_{digest}"


def public_customer_label(_: str | None) -> str:
    """Do not expose customer identifiers in the operator UI/API."""
    return "Protected account"


def _sensitive_key(key: object) -> bool:
    normalized = str(key).lower().replace("-", "_")
    return (
        normalized in _SENSITIVE_KEYS
        or normalized.endswith("_email")
        or normalized.endswith("_phone")
        or normalized.endswith("_url")
        or normalized.endswith("_token")
        or normalized.endswith("_secret")
    )


def redact_sensitive(value: Any) -> Any:
    """Recursively replace sensitive values while retaining useful evidence."""
    if isinstance(value, Mapping):
        return {
            str(key): "[redacted]" if _sensitive_key(key) else redact_sensitive(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, tuple):
        return [redact_sensitive(item) for item in value]
    return value


def safe_subscription(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Allowlist operational subscription fields from an upstream response."""
    fields = (
        "id",
        "status",
        "plan_id",
        "quantity",
        "total_count",
        "paid_count",
        "remaining_count",
        "charge_at",
        "current_start",
        "current_end",
        "start_at",
        "end_at",
        "expire_by",
        "created_at",
    )
    return {field: payload[field] for field in fields if field in payload}


def safe_invoice_collection(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Allowlist invoice state and value fields, excluding customer/payment data."""
    item_fields = (
        "id",
        "status",
        "type",
        "subscription_id",
        "amount",
        "amount_paid",
        "amount_due",
        "currency",
        "paid_at",
        "issued_at",
        "expired_at",
        "created_at",
    )
    items = payload.get("items")
    safe_items = []
    if isinstance(items, list):
        for item in items:
            if isinstance(item, Mapping):
                safe_items.append({field: item[field] for field in item_fields if field in item})
    count = payload.get("count")
    return {"count": int(count) if isinstance(count, int) else len(safe_items), "items": safe_items}

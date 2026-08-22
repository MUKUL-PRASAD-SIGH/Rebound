"""Append-only audit trail helpers."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from rebound.db.models import AuditEvent
from rebound.schemas.enums import AuditKind


def append_audit(db: Session, case_id: str, kind: AuditKind | str, payload: dict[str, Any]) -> AuditEvent:
    event = AuditEvent(
        case_id=case_id,
        kind=kind.value if isinstance(kind, AuditKind) else kind,
        payload_json=json.dumps(payload),
    )
    db.add(event)
    return event

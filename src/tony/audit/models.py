"""Audit models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class AuditRecord(BaseModel):
    """Represents a single audit record."""

    model_config = ConfigDict(
        frozen=True,
    )

    tool: str
    success: bool
    duration_ms: float

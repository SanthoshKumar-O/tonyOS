"""Execution models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ExecutionStatus(StrEnum):
    """Execution status."""

    STARTED = "started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionEvent(BaseModel):
    """Execution event."""

    model_config = ConfigDict(frozen=True)

    status: ExecutionStatus
    tool: str


class ExecutionMetrics(BaseModel):
    """Execution metrics."""

    model_config = ConfigDict(frozen=True)

    duration_ms: float

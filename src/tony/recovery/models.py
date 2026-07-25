"""Recovery models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class RecoveryAction(StrEnum):
    """Recovery actions."""

    RETRY = "retry"
    IGNORE = "ignore"
    REPORT = "report"
    ABORT = "abort"


class RecoveryDecision(BaseModel):
    """Recovery decision."""

    model_config = ConfigDict(frozen=True)

    action: RecoveryAction
    reason: str

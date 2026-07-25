"""Recovery protocols."""

from __future__ import annotations

from typing import Protocol

from .models import RecoveryDecision


class RecoveryEngineProtocol(Protocol):
    """Protocol for recovery engines."""

    def recover(
        self,
        error: str,
    ) -> RecoveryDecision: ...

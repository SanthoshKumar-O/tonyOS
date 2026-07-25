"""Recovery engine."""

from __future__ import annotations

from .models import (
    RecoveryAction,
    RecoveryDecision,
)
from .protocols import RecoveryEngineProtocol


class RecoveryEngine(RecoveryEngineProtocol):
    """Determines how execution failures should be handled."""

    def recover(
        self,
        error: str,
    ) -> RecoveryDecision:
        """Determine the appropriate recovery action."""

        message = error.lower()

        if "already exists" in message:
            return RecoveryDecision(
                action=RecoveryAction.IGNORE,
                reason="Resource already exists.",
            )

        if "no such file" in message:
            return RecoveryDecision(
                action=RecoveryAction.REPORT,
                reason="Requested file was not found.",
            )

        if "index.lock" in message:
            return RecoveryDecision(
                action=RecoveryAction.RETRY,
                reason="Repository is temporarily locked.",
            )

        return RecoveryDecision(
            action=RecoveryAction.ABORT,
            reason="Unrecoverable error.",
        )

"""Tests for recovery models."""

from __future__ import annotations

from tony.recovery import (
    RecoveryAction,
    RecoveryDecision,
)


def test_recovery_decision() -> None:
    decision = RecoveryDecision(
        action=RecoveryAction.RETRY,
        reason="Retry later.",
    )

    assert decision.action == RecoveryAction.RETRY
    assert decision.reason == "Retry later."

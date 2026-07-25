"""Tests for the recovery engine."""

from __future__ import annotations

from tony.recovery import (
    RecoveryAction,
    RecoveryEngine,
)


def test_ignore_existing_resource() -> None:
    engine = RecoveryEngine()

    decision = engine.recover(
        "File already exists",
    )

    assert decision.action == RecoveryAction.IGNORE
    assert decision.reason == "Resource already exists."


def test_report_missing_file() -> None:
    engine = RecoveryEngine()

    decision = engine.recover(
        "No such file or directory",
    )

    assert decision.action == RecoveryAction.REPORT
    assert decision.reason == "Requested file was not found."


def test_retry_locked_repository() -> None:
    engine = RecoveryEngine()

    decision = engine.recover(
        "Unable to create '.git/index.lock'",
    )

    assert decision.action == RecoveryAction.RETRY
    assert decision.reason == "Repository is temporarily locked."


def test_abort_unknown_error() -> None:
    engine = RecoveryEngine()

    decision = engine.recover(
        "Unexpected runtime failure",
    )

    assert decision.action == RecoveryAction.ABORT
    assert decision.reason == "Unrecoverable error."

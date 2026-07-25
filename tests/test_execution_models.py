"""Tests for execution models."""

from __future__ import annotations

from tony.execution import (
    ExecutionEvent,
    ExecutionMetrics,
    ExecutionStatus,
)


def test_execution_event() -> None:
    event = ExecutionEvent(
        status=ExecutionStatus.STARTED,
        tool="pwd",
    )

    assert event.status == ExecutionStatus.STARTED
    assert event.tool == "pwd"


def test_execution_metrics() -> None:
    metrics = ExecutionMetrics(
        duration_ms=12.5,
    )

    assert metrics.duration_ms == 12.5

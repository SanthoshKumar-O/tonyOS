"""Tests for the execution monitor."""

from __future__ import annotations

from tony.execution import (
    ExecutionMonitor,
    ExecutionStatus,
)


def test_start_event() -> None:
    monitor = ExecutionMonitor()

    event = monitor.start("pwd")

    assert event.status == ExecutionStatus.STARTED
    assert event.tool == "pwd"


def test_complete_event() -> None:
    monitor = ExecutionMonitor()

    event = monitor.complete("pwd")

    assert event.status == ExecutionStatus.COMPLETED
    assert event.tool == "pwd"


def test_fail_event() -> None:
    monitor = ExecutionMonitor()

    event = monitor.fail("pwd")

    assert event.status == ExecutionStatus.FAILED
    assert event.tool == "pwd"

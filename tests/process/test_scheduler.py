"""Tests for ProcessSchedulerTool."""

from __future__ import annotations

import os
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessSchedulerTool


def test_metadata() -> None:
    tool = ProcessSchedulerTool()

    assert tool.metadata.name == "process_scheduler"


def test_missing_pid() -> None:
    tool = ProcessSchedulerTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.scheduler.os.getpriority")
@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_returns_scheduler_information(
    mock_scheduler,
    mock_priority,
) -> None:
    mock_scheduler.return_value = os.SCHED_OTHER
    mock_priority.return_value = 0

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == (
        "policy: SCHED_OTHER\n"
        "priority: 0"
    )
    assert result.exit_code == 0

    mock_scheduler.assert_called_once_with(123)
    mock_priority.assert_called_once_with(os.PRIO_PROCESS, 123)


@patch("tony.tools.process.scheduler.os.getpriority")
@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_returns_fifo_policy(
    mock_scheduler,
    mock_priority,
) -> None:
    mock_scheduler.return_value = os.SCHED_FIFO
    mock_priority.return_value = 10

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "policy: SCHED_FIFO" in result.output
    assert "priority: 10" in result.output


@patch("tony.tools.process.scheduler.os.getpriority")
@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_unknown_policy_is_returned_numerically(
    mock_scheduler,
    mock_priority,
) -> None:
    mock_scheduler.return_value = 999
    mock_priority.return_value = 0

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "policy: 999" in result.output


@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_process_not_found(mock_scheduler) -> None:
    mock_scheduler.side_effect = ProcessLookupError

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_permission_denied(mock_scheduler) -> None:
    mock_scheduler.side_effect = PermissionError

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading scheduler information for process '123'."
    )


@patch("tony.tools.process.scheduler.os.sched_getscheduler")
def test_os_error(mock_scheduler) -> None:
    mock_scheduler.side_effect = OSError("scheduler unavailable")

    tool = ProcessSchedulerTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "scheduler unavailable"
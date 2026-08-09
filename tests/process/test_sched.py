"""Tests for ProcessSchedTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessSchedTool


def test_metadata() -> None:
    tool = ProcessSchedTool()

    assert tool.metadata.name == "process_sched"


def test_missing_pid() -> None:
    tool = ProcessSchedTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.sched.Path.read_text")
def test_returns_scheduler_statistics(mock_read_text) -> None:
    mock_read_text.return_value = (
        "python (123, #threads: 4)\n"
        "se.exec_start : 123456789\n"
        "se.sum_exec_runtime : 98765.000000\n"
        "nr_switches : 42\n"
    )

    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "se.exec_start" in result.output
    assert "se.sum_exec_runtime" in result.output
    assert "nr_switches" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.sched.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "nr_switches : 42\n"

    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "nr_switches : 42"


@patch("tony.tools.process.sched.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.sched.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading scheduler statistics of process '123'."
    )


@patch("tony.tools.process.sched.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessSchedTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
"""Tests for ProcessStatusFlagsTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessStatusFlagsTool


def test_metadata() -> None:
    tool = ProcessStatusFlagsTool()

    assert tool.metadata.name == "process_status_flags"


def test_missing_pid() -> None:
    tool = ProcessStatusFlagsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.status_flags.Path.read_text")
def test_returns_process_state(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "Umask:\t0022\n"
        "State:\tS (sleeping)\n"
        "Pid:\t123\n"
    )

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "S (sleeping)"
    assert result.exit_code == 0


@patch("tony.tools.process.status_flags.Path.read_text")
def test_returns_running_state(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "State:\tR (running)\n"
    )

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "R (running)"


@patch("tony.tools.process.status_flags.Path.read_text")
def test_state_missing(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "Pid:\t123\n"
    )

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "State information is unavailable for process '123'."


@patch("tony.tools.process.status_flags.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.status_flags.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Permission denied reading status of process '123'."


@patch("tony.tools.process.status_flags.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessStatusFlagsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
"""Tests for ProcessStatusTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessStatusTool


def test_metadata() -> None:
    tool = ProcessStatusTool()

    assert tool.metadata.name == "process_status"


def test_missing_pid() -> None:
    tool = ProcessStatusTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.status.Path.read_text")
def test_returns_process_status(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "State:\tS (sleeping)\n"
        "Pid:\t123\n"
        "PPid:\t1\n"
        "Threads:\t4\n"
        "VmRSS:\t10240 kB\n"
    )

    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "Name:" in result.output
    assert "python" in result.output
    assert "State:" in result.output
    assert "Threads:" in result.output
    assert "VmRSS:" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.status.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "Name:\tpython\n"

    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "Name:\tpython"


@patch("tony.tools.process.status.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.status.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Permission denied reading status of process '123'."


@patch("tony.tools.process.status.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessStatusTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
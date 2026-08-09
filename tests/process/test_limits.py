"""Tests for ProcessLimitsTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessLimitsTool


def test_metadata() -> None:
    tool = ProcessLimitsTool()

    assert tool.metadata.name == "process_limits"


def test_missing_pid() -> None:
    tool = ProcessLimitsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.limits.Path.read_text")
def test_returns_limits(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Limit                     Soft Limit           Hard Limit           Units\n"
        "Max open files            1024                 4096                 files\n"
        "Max processes             1000                 1000                 processes\n"
    )

    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "Max open files" in result.output
    assert "1024" in result.output
    assert "4096" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.limits.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "Max open files 1024 4096 files\n"

    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "Max open files 1024 4096 files"


@patch("tony.tools.process.limits.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.limits.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Permission denied reading limits of process '123'."


@patch("tony.tools.process.limits.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessLimitsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
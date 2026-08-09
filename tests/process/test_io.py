"""Tests for ProcessIOTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessIOTool


def test_metadata() -> None:
    tool = ProcessIOTool()

    assert tool.metadata.name == "process_io"


def test_missing_pid() -> None:
    tool = ProcessIOTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.io.Path.read_text")
def test_returns_io_statistics(mock_read_text) -> None:
    mock_read_text.return_value = (
        "rchar: 123456\n"
        "wchar: 654321\n"
        "syscr: 100\n"
        "syscw: 80\n"
        "read_bytes: 4096\n"
        "write_bytes: 8192\n"
        "cancelled_write_bytes: 0\n"
    )

    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "rchar: 123456" in result.output
    assert "wchar: 654321" in result.output
    assert "read_bytes: 4096" in result.output
    assert "write_bytes: 8192" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.io.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "read_bytes: 4096\n"

    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "read_bytes: 4096"


@patch("tony.tools.process.io.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.io.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading I/O statistics of process '123'."
    )


@patch("tony.tools.process.io.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessIOTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
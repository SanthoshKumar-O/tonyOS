"""Tests for ProcessCommandLineTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessCommandLineTool


def test_metadata() -> None:
    tool = ProcessCommandLineTool()

    assert tool.metadata.name == "process_command_line"


def test_missing_pid() -> None:
    tool = ProcessCommandLineTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_returns_command_line(mock_read_bytes) -> None:
    mock_read_bytes.return_value = (
        b"python\x00-m\x00http.server\x008000\x00"
    )

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "python -m http.server 8000"
    assert result.exit_code == 0


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_empty_command_line(mock_read_bytes) -> None:
    mock_read_bytes.return_value = b""

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == ""


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_non_utf8_command_line(mock_read_bytes) -> None:
    mock_read_bytes.return_value = b"program\x00--value\x00\xff\x00"

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output.startswith("program --value")


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_process_not_found(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = FileNotFoundError

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_permission_denied(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = PermissionError

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading command line of process '123'."
    )


@patch("tony.tools.process.command_line.Path.read_bytes")
def test_os_error(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = OSError("proc unavailable")

    tool = ProcessCommandLineTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
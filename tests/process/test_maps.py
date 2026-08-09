"""Tests for ProcessMapsTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessMapsTool


def test_metadata() -> None:
    tool = ProcessMapsTool()

    assert tool.metadata.name == "process_maps"


def test_missing_pid() -> None:
    tool = ProcessMapsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.maps.Path.read_text")
def test_returns_memory_maps(mock_read_text) -> None:
    mock_read_text.return_value = (
        "555555-556000 r--p 00000000 08:01 12345 /usr/bin/python\n"
        "556000-557000 r-xp 00001000 08:01 12345 /usr/bin/python\n"
        "7fff0000-80000000 rw-p 00000000 00:00 0 [stack]\n"
    )

    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "/usr/bin/python" in result.output
    assert "[stack]" in result.output
    assert "r-xp" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.maps.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "1000-2000 rw-p 00000000 00:00 0 [heap]\n"

    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "1000-2000 rw-p 00000000 00:00 0 [heap]"


@patch("tony.tools.process.maps.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.maps.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading memory maps of process '123'."
    )


@patch("tony.tools.process.maps.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessMapsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
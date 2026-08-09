"""Tests for ProcessFdsTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessFdsTool


def test_metadata() -> None:
    tool = ProcessFdsTool()

    assert tool.metadata.name == "process_fds"


def test_missing_pid() -> None:
    tool = ProcessFdsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.fds.Path.iterdir")
def test_returns_file_descriptors(mock_iterdir) -> None:
    stdin_fd = Path("/proc/123/fd/0")
    stdout_fd = Path("/proc/123/fd/1")

    mock_iterdir.return_value = [
        stdout_fd,
        stdin_fd,
    ]

    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "0:" in result.output
    assert "1:" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.fds.Path.iterdir")
def test_process_not_found(mock_iterdir) -> None:
    mock_iterdir.side_effect = FileNotFoundError

    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.fds.Path.iterdir")
def test_permission_denied(mock_iterdir) -> None:
    mock_iterdir.side_effect = PermissionError

    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading file descriptors of process '123'."
    )


@patch("tony.tools.process.fds.Path.iterdir")
def test_os_error(mock_iterdir) -> None:
    mock_iterdir.side_effect = OSError("proc unavailable")

    tool = ProcessFdsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
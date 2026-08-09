"""Tests for ProcessNamespacesTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessNamespacesTool


def test_metadata() -> None:
    tool = ProcessNamespacesTool()

    assert tool.metadata.name == "process_namespaces"


def test_missing_pid() -> None:
    tool = ProcessNamespacesTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.namespaces.Path.iterdir")
def test_returns_namespaces(mock_iterdir) -> None:
    pid_ns = Path("/proc/123/ns/pid")
    net_ns = Path("/proc/123/ns/net")

    mock_iterdir.return_value = [net_ns, pid_ns]

    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "pid:" in result.output
    assert "net:" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.namespaces.Path.iterdir")
def test_process_not_found(mock_iterdir) -> None:
    mock_iterdir.side_effect = FileNotFoundError

    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.namespaces.Path.iterdir")
def test_permission_denied(mock_iterdir) -> None:
    mock_iterdir.side_effect = PermissionError

    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading namespaces of process '123'."
    )


@patch("tony.tools.process.namespaces.Path.iterdir")
def test_os_error(mock_iterdir) -> None:
    mock_iterdir.side_effect = OSError("proc unavailable")

    tool = ProcessNamespacesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
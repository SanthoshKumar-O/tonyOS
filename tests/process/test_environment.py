"""Tests for ProcessEnvironmentTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessEnvironmentTool


def test_metadata() -> None:
    tool = ProcessEnvironmentTool()

    assert tool.metadata.name == "process_environment"


def test_missing_pid() -> None:
    tool = ProcessEnvironmentTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.environment.Path.read_bytes")
def test_returns_environment(mock_read_bytes) -> None:
    mock_read_bytes.return_value = (
        b"ZEBRA=value2\0ALPHA=value1\0PATH=/usr/bin\0"
    )

    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == (
        "ALPHA=value1\n"
        "PATH=/usr/bin\n"
        "ZEBRA=value2"
    )


@patch("tony.tools.process.environment.Path.read_bytes")
def test_empty_environment(mock_read_bytes) -> None:
    mock_read_bytes.return_value = b""

    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == ""


@patch("tony.tools.process.environment.Path.read_bytes")
def test_process_not_found(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = FileNotFoundError

    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.environment.Path.read_bytes")
def test_permission_denied(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = PermissionError

    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading environment of process '123'."
    )


@patch("tony.tools.process.environment.Path.read_bytes")
def test_os_error(mock_read_bytes) -> None:
    mock_read_bytes.side_effect = OSError("proc unavailable")

    tool = ProcessEnvironmentTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
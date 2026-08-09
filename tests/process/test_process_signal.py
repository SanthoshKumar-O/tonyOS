"""Tests for ProcessSignalTool."""

from __future__ import annotations

import signal
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessSignalTool


def test_metadata() -> None:
    tool = ProcessSignalTool()

    assert tool.metadata.name == "process_signal"


def test_missing_arguments() -> None:
    result = ProcessSignalTool().execute([])

    assert result.success is False
    assert result.error == "Process ID and signal are required."


def test_missing_signal() -> None:
    result = ProcessSignalTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Process ID and signal are required."


def test_invalid_pid() -> None:
    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="abc"),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_empty_pid() -> None:
    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value=""),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_unknown_signal() -> None:
    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="signal", value="NOT_A_SIGNAL"),
        ]
    )

    assert result.success is False
    assert result.error == "Unknown signal 'NOT_A_SIGNAL'."


@patch("tony.tools.process.process_signal.os.kill")
def test_send_signal(mock_kill) -> None:
    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is True
    assert result.output == "Sent SIGTERM to process '123'."
    mock_kill.assert_called_once_with(123, signal.SIGTERM)


@patch("tony.tools.process.process_signal.os.kill")
def test_signal_with_sig_prefix(mock_kill) -> None:
    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="signal", value="SIGKILL"),
        ]
    )

    assert result.success is True
    assert result.output == "Sent SIGKILL to process '123'."
    mock_kill.assert_called_once_with(123, signal.SIGKILL)


@patch("tony.tools.process.process_signal.os.kill")
def test_process_not_found(mock_kill) -> None:
    mock_kill.side_effect = ProcessLookupError

    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="999999"),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.process_signal.os.kill")
def test_permission_denied(mock_kill) -> None:
    mock_kill.side_effect = PermissionError

    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied sending SIGTERM to process '123'."
    )


@patch("tony.tools.process.process_signal.os.kill")
def test_os_error(mock_kill) -> None:
    mock_kill.side_effect = OSError("signal failed")

    result = ProcessSignalTool().execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="signal", value="TERM"),
        ]
    )

    assert result.success is False
    assert result.error == "signal failed"
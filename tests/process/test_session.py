"""Tests for ProcessSessionTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessSessionTool


def test_metadata() -> None:
    tool = ProcessSessionTool()

    assert tool.metadata.name == "process_session"


def test_missing_pid() -> None:
    result = ProcessSessionTool().execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.session.Path.read_text")
@patch("tony.tools.process.session.os.getpgid")
@patch("tony.tools.process.session.os.getsid")
def test_returns_session_information(
    mock_getsid,
    mock_getpgid,
    mock_read_text,
) -> None:
    mock_getsid.return_value = 100
    mock_getpgid.return_value = 200
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "PPid:\t50\n"
    )

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == (
        "pid: 123\n"
        "ppid: 50\n"
        "pgid: 200\n"
        "sid: 100"
    )


@patch("tony.tools.process.session.Path.read_text")
@patch("tony.tools.process.session.os.getpgid")
@patch("tony.tools.process.session.os.getsid")
def test_missing_parent_pid(
    mock_getsid,
    mock_getpgid,
    mock_read_text,
) -> None:
    mock_getsid.return_value = 100
    mock_getpgid.return_value = 200
    mock_read_text.return_value = "Name:\tpython\n"

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "ppid: 0" in result.output


@patch("tony.tools.process.session.os.getsid")
def test_process_not_found(mock_getsid) -> None:
    mock_getsid.side_effect = ProcessLookupError

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.session.os.getsid")
def test_permission_denied(mock_getsid) -> None:
    mock_getsid.side_effect = PermissionError

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == (
        "Permission denied reading session of process '123'."
    )


@patch("tony.tools.process.session.os.getsid")
def test_os_error(mock_getsid) -> None:
    mock_getsid.side_effect = OSError("session unavailable")

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "session unavailable"


@patch("tony.tools.process.session.Path.read_text")
@patch("tony.tools.process.session.os.getpgid")
@patch("tony.tools.process.session.os.getsid")
def test_status_file_not_found(
    mock_getsid,
    mock_getpgid,
    mock_read_text,
) -> None:
    mock_getsid.return_value = 100
    mock_getpgid.return_value = 200
    mock_read_text.side_effect = FileNotFoundError

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Process '123' was not found."


@patch("tony.tools.process.session.Path.read_text")
@patch("tony.tools.process.session.os.getpgid")
@patch("tony.tools.process.session.os.getsid")
def test_status_permission_denied(
    mock_getsid,
    mock_getpgid,
    mock_read_text,
) -> None:
    mock_getsid.return_value = 100
    mock_getpgid.return_value = 200
    mock_read_text.side_effect = PermissionError

    result = ProcessSessionTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == (
        "Permission denied reading session of process '123'."
    )
"""Tests for ProcessIdentityTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessIdentityTool


def test_metadata() -> None:
    tool = ProcessIdentityTool()

    assert tool.metadata.name == "process_identity"


def test_missing_pid() -> None:
    result = ProcessIdentityTool().execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    result = ProcessIdentityTool().execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    result = ProcessIdentityTool().execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    result = ProcessIdentityTool().execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.identity.ProcessIdentityTool._username")
@patch("tony.tools.process.identity.Path.read_text")
def test_returns_identity(mock_read_text, mock_username) -> None:
    mock_read_text.return_value = (
        "Name:\tpython\n"
        "Uid:\t1000\t1000\t1000\t1000\n"
        "Gid:\t1000\t1000\t1000\t1000\n"
    )
    mock_username.return_value = "santhoshkumar"

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "uid: 1000" in result.output
    assert "euid: 1000" in result.output
    assert "user: santhoshkumar" in result.output
    assert "gid: 1000" in result.output
    assert "egid: 1000" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.identity.Path.read_text")
def test_identity_information_missing(mock_read_text) -> None:
    mock_read_text.return_value = "Name:\tpython\n"

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Identity information is unavailable for process '123'."
    )


@patch("tony.tools.process.identity.Path.read_text")
def test_invalid_uid_data(mock_read_text) -> None:
    mock_read_text.return_value = (
        "Uid:\tnot-a-number\n"
        "Gid:\t1000\t1000\t1000\t1000\n"
    )

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Identity information is unavailable for process '123'."
    )


@patch("tony.tools.process.identity.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.identity.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Permission denied reading identity of process '123'."


@patch("tony.tools.process.identity.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessIdentityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"


@patch("tony.tools.process.identity.pwd.getpwuid")
def test_unknown_uid(mock_getpwuid) -> None:
    mock_getpwuid.side_effect = KeyError

    assert ProcessIdentityTool._username(99999) == "99999"
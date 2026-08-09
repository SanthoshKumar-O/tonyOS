"""Tests for ProcessCgroupTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessCgroupTool


def test_metadata() -> None:
    tool = ProcessCgroupTool()

    assert tool.metadata.name == "process_cgroup"


def test_missing_pid() -> None:
    tool = ProcessCgroupTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.cgroup.Path.read_text")
def test_returns_cgroup_information(mock_read_text) -> None:
    mock_read_text.return_value = (
        "0::/user.slice/user-1000.slice/session-1.scope\n"
    )

    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "user.slice" in result.output
    assert "session-1.scope" in result.output
    assert result.exit_code == 0


@patch("tony.tools.process.cgroup.Path.read_text")
def test_trailing_newline_is_removed(mock_read_text) -> None:
    mock_read_text.return_value = "0::/system.slice/example.service\n"

    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "0::/system.slice/example.service"


@patch("tony.tools.process.cgroup.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.cgroup.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading control groups of process '123'."
    )


@patch("tony.tools.process.cgroup.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    tool = ProcessCgroupTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
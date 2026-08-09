"""Tests for ProcessRootDirectoryTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessRootDirectoryTool


def test_metadata() -> None:
    tool = ProcessRootDirectoryTool()

    assert tool.metadata.name == "process_root_directory"


def test_missing_pid() -> None:
    tool = ProcessRootDirectoryTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.root_directory.Path.resolve")
def test_returns_root_directory(mock_resolve) -> None:
    mock_resolve.return_value = Path("/")

    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "/"

    mock_resolve.assert_called_once_with(strict=True)


@patch("tony.tools.process.root_directory.Path.resolve")
def test_returns_container_root(mock_resolve) -> None:
    mock_resolve.return_value = Path("/var/lib/container/rootfs")

    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="456")]
    )

    assert result.success is True
    assert result.output == "/var/lib/container/rootfs"


@patch("tony.tools.process.root_directory.Path.resolve")
def test_process_not_found(mock_resolve) -> None:
    mock_resolve.side_effect = FileNotFoundError

    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.root_directory.Path.resolve")
def test_permission_denied(mock_resolve) -> None:
    mock_resolve.side_effect = PermissionError

    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading root directory of process '123'."
    )


@patch("tony.tools.process.root_directory.Path.resolve")
def test_os_error(mock_resolve) -> None:
    mock_resolve.side_effect = OSError("proc unavailable")

    tool = ProcessRootDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
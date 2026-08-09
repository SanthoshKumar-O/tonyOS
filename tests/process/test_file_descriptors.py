"""Tests for ProcessFileDescriptorsTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessFileDescriptorsTool


def test_metadata() -> None:
    tool = ProcessFileDescriptorsTool()

    assert tool.metadata.name == "process_file_descriptors"


def test_missing_pid() -> None:
    tool = ProcessFileDescriptorsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.file_descriptors.Path.iterdir")
def test_returns_file_descriptors(mock_iterdir) -> None:
    fd1 = MagicMock(spec=Path)
    fd1.name = "0"

    fd2 = MagicMock(spec=Path)
    fd2.name = "1"

    fd3 = MagicMock(spec=Path)
    fd3.name = "2"

    fd1.resolve.return_value = Path("/dev/null")
    fd2.resolve.return_value = Path("/home/user/input.txt")
    fd3.resolve.return_value = Path("/tmp/output.txt")

    mock_iterdir.return_value = [
        fd2,
        fd3,
        fd1,
    ]

    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == (
        "0 -> /dev/null\n"
        "1 -> /home/user/input.txt\n"
        "2 -> /tmp/output.txt"
    )


@patch("tony.tools.process.file_descriptors.Path.iterdir")
def test_process_not_found(mock_iterdir) -> None:
    mock_iterdir.side_effect = FileNotFoundError

    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.file_descriptors.Path.iterdir")
def test_permission_denied(mock_iterdir) -> None:
    mock_iterdir.side_effect = PermissionError

    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading file descriptors of process '123'."
    )


@patch("tony.tools.process.file_descriptors.Path.iterdir")
def test_os_error(mock_iterdir) -> None:
    mock_iterdir.side_effect = OSError("proc unavailable")

    tool = ProcessFileDescriptorsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"
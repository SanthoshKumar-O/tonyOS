"""Tests for ProcessOpenFilesTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessOpenFilesTool


def test_metadata() -> None:
    tool = ProcessOpenFilesTool()

    assert tool.metadata.name == "process_open_files"


def test_missing_pid() -> None:
    tool = ProcessOpenFilesTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.open_files.subprocess.run")
def test_returns_open_files(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\n"
        "python 123 user cwd DIR 8,1 4096 123 /home/user/app\n"
        "python 123 user 3r REG 8,1 1000 456 /tmp/data.txt\n"
    )
    mock_run.return_value.stderr = ""

    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "/home/user/app" in result.output
    assert "/tmp/data.txt" in result.output

    mock_run.assert_called_once_with(
        [
            "lsof",
            "-p",
            "123",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.open_files.subprocess.run")
def test_lsof_failure(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = "Permission denied"

    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Permission denied"
    assert result.exit_code == 1


@patch("tony.tools.process.open_files.subprocess.run")
def test_lsof_not_available(mock_run) -> None:
    mock_run.side_effect = OSError("lsof not found")

    tool = ProcessOpenFilesTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "lsof not found"
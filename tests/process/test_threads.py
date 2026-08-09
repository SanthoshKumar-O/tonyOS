"""Tests for ProcessThreadsTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessThreadsTool


def test_metadata() -> None:
    tool = ProcessThreadsTool()

    assert tool.metadata.name == "process_threads"


def test_missing_pid() -> None:
    tool = ProcessThreadsTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.threads.subprocess.run")
def test_returns_threads(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "123 123 1.2 Sl python\n"
        "123 124 0.3 Sl worker\n"
        "123 125 0.1 Sl worker\n"
    )
    mock_run.return_value.stderr = ""

    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "123 123" in result.output
    assert "123 124" in result.output
    assert "123 125" in result.output
    assert "worker" in result.output

    mock_run.assert_called_once_with(
        [
            "ps",
            "-T",
            "-p",
            "123",
            "-o",
            "pid=,spid=,pcpu=,stat=,comm=",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.threads.subprocess.run")
def test_process_not_found(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = ""

    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."
    assert result.exit_code == 1


@patch("tony.tools.process.threads.subprocess.run")
def test_ps_error(mock_run) -> None:
    mock_run.side_effect = OSError("ps not found")

    tool = ProcessThreadsTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "ps not found"
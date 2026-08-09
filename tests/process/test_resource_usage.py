"""Tests for ProcessResourceUsageTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessResourceUsageTool


def test_metadata() -> None:
    tool = ProcessResourceUsageTool()

    assert tool.metadata.name == "process_resource_usage"


def test_missing_pid() -> None:
    tool = ProcessResourceUsageTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.resource_usage.subprocess.run")
def test_returns_resource_usage(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "123 12.5 3.2 45678 123456 00:10:00 python app.py\n"
    )
    mock_run.return_value.stderr = ""

    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "12.5" in result.output
    assert "3.2" in result.output
    assert "python app.py" in result.output

    mock_run.assert_called_once_with(
        [
            "ps",
            "-p",
            "123",
            "-o",
            "pid=,pcpu=,pmem=,rss=,vsz=,etime=,cmd=",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.resource_usage.subprocess.run")
def test_process_not_found(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = ""

    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."
    assert result.exit_code == 1


@patch("tony.tools.process.resource_usage.subprocess.run")
def test_ps_error(mock_run) -> None:
    mock_run.side_effect = OSError("ps not found")

    tool = ProcessResourceUsageTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "ps not found"
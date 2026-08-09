"""Tests for InspectProcessTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import InspectProcessTool


def test_metadata() -> None:
    tool = InspectProcessTool()

    assert tool.metadata.name == "inspect_process"


def test_missing_pid() -> None:
    tool = InspectProcessTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = InspectProcessTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = InspectProcessTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = InspectProcessTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.inspect_process.subprocess.run")
def test_inspects_process(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "123 1 user S 00:10:00 python app.py\n"
    )
    mock_run.return_value.stderr = ""

    tool = InspectProcessTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "123" in result.output
    assert "python app.py" in result.output

    mock_run.assert_called_once_with(
        [
            "ps",
            "-p",
            "123",
            "-o",
            "pid=,ppid=,user=,stat=,etime=,cmd=",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.inspect_process.subprocess.run")
def test_process_not_found(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = ""

    tool = InspectProcessTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."
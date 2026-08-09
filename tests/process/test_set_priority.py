"""Tests for SetProcessPriorityTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import SetProcessPriorityTool


def test_metadata() -> None:
    tool = SetProcessPriorityTool()

    assert tool.metadata.name == "set_process_priority"


def test_missing_arguments() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID and priority are required."


def test_missing_priority() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "Process ID and priority are required."


def test_invalid_pid() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="abc"),
            ToolArgument(name="priority", value="10"),
        ]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="0"),
            ToolArgument(name="priority", value="10"),
        ]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_invalid_priority() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="priority", value="abc"),
        ]
    )

    assert result.success is False
    assert result.error == "Priority must be an integer."


def test_priority_below_range() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="priority", value="-21"),
        ]
    )

    assert result.success is False
    assert result.error == "Priority must be between -20 and 19."


def test_priority_above_range() -> None:
    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="priority", value="20"),
        ]
    )

    assert result.success is False
    assert result.error == "Priority must be between -20 and 19."


@patch("tony.tools.process.set_priority.subprocess.run")
def test_sets_process_priority(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "123 (process ID) old priority 0, new priority 10\n"
    )
    mock_run.return_value.stderr = ""

    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="priority", value="10"),
        ]
    )

    assert result.success is True
    assert "new priority 10" in result.output

    mock_run.assert_called_once_with(
        [
            "renice",
            "10",
            "-p",
            "123",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.set_priority.subprocess.run")
def test_renice_failure(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = "Permission denied"

    tool = SetProcessPriorityTool()

    result = tool.execute(
        [
            ToolArgument(name="pid", value="123"),
            ToolArgument(name="priority", value="10"),
        ]
    )

    assert result.success is False
    assert result.error == "Permission denied"
    assert result.exit_code == 1
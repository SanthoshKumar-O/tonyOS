"""Tests for ProcessAffinityTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessAffinityTool


def test_metadata() -> None:
    tool = ProcessAffinityTool()

    assert tool.metadata.name == "process_affinity"


def test_missing_pid() -> None:
    tool = ProcessAffinityTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.affinity.os.sched_getaffinity")
def test_returns_cpu_affinity(mock_affinity) -> None:
    mock_affinity.return_value = {3, 1, 7, 2}

    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "1,2,3,7"
    assert result.exit_code == 0

    mock_affinity.assert_called_once_with(123)


@patch("tony.tools.process.affinity.os.sched_getaffinity")
def test_single_cpu(mock_affinity) -> None:
    mock_affinity.return_value = {4}

    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == "4"


@patch("tony.tools.process.affinity.os.sched_getaffinity")
def test_process_not_found(mock_affinity) -> None:
    mock_affinity.side_effect = ProcessLookupError

    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.affinity.os.sched_getaffinity")
def test_permission_denied(mock_affinity) -> None:
    mock_affinity.side_effect = PermissionError

    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Permission denied reading CPU affinity of process '123'."
    )


@patch("tony.tools.process.affinity.os.sched_getaffinity")
def test_os_error(mock_affinity) -> None:
    mock_affinity.side_effect = OSError("affinity unavailable")

    tool = ProcessAffinityTool()

    result = tool.execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "affinity unavailable"
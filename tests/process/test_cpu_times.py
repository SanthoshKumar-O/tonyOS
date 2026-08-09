"""Tests for ProcessCpuTimesTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessCpuTimesTool


def test_metadata() -> None:
    tool = ProcessCpuTimesTool()

    assert tool.metadata.name == "process_cpu_times"


def test_missing_pid() -> None:
    result = ProcessCpuTimesTool().execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_returns_cpu_times(mock_read_text) -> None:
    # Fields after the command name begin at field 3.
    # State is field 3, utime is field 14, stime is field 15.
    fields = ["R"] + ["0"] * 10 + ["100", "25"]

    mock_read_text.return_value = (
        "123 (python process) " + " ".join(fields)
    )

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert result.output == (
        "user_ticks: 100\n"
        "system_ticks: 25\n"
        "total_ticks: 125"
    )


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_process_name_with_spaces(mock_read_text) -> None:
    fields = ["S"] + ["0"] * 10 + ["50", "20"]

    mock_read_text.return_value = (
        "123 (my python process) " + " ".join(fields)
    )

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "user_ticks: 50" in result.output
    assert "system_ticks: 20" in result.output
    assert "total_ticks: 70" in result.output


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == (
        "Permission denied reading CPU times of process '123'."
    )


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"


@patch("tony.tools.process.cpu_times.Path.read_text")
def test_malformed_stat(mock_read_text) -> None:
    mock_read_text.return_value = "123 (python)"

    result = ProcessCpuTimesTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "CPU time information is unavailable for process '123'."
    )

"""Tests for ProcessStatsTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.process import ProcessStatsTool


def test_metadata() -> None:
    tool = ProcessStatsTool()

    assert tool.metadata.name == "process_stats"


def test_missing_pid() -> None:
    result = ProcessStatsTool().execute([])

    assert result.success is False
    assert result.error == "Process ID is required."


def test_empty_pid() -> None:
    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="")]
    )

    assert result.success is False
    assert result.error == "Process ID cannot be empty."


def test_invalid_pid() -> None:
    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="abc")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


def test_zero_pid() -> None:
    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="0")]
    )

    assert result.success is False
    assert result.error == "Process ID must be a positive integer."


@patch("tony.tools.process.stats.Path.read_text")
def test_returns_stats(mock_read_text) -> None:
    fields = ["0"] * 22

    fields[0] = "S"       # state
    fields[1] = "10"      # ppid
    fields[2] = "20"      # pgid
    fields[3] = "30"      # session
    fields[16] = "4"      # threads
    fields[19] = "12345"  # start_time
    fields[20] = "4096"   # virtual_memory
    fields[21] = "128"    # resident_pages

    mock_read_text.return_value = (
        "123 (python process) " + " ".join(fields)
    )

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "pid: 123" in result.output
    assert "state: S" in result.output
    assert "ppid: 10" in result.output
    assert "pgid: 20" in result.output
    assert "sid: 30" in result.output
    assert "threads: 4" in result.output
    assert "start_time: 12345" in result.output
    assert "virtual_memory: 4096" in result.output
    assert "resident_pages: 128" in result.output


@patch("tony.tools.process.stats.Path.read_text")
def test_process_name_with_spaces(mock_read_text) -> None:
    fields = ["0"] * 22

    fields[0] = "R"
    fields[16] = "2"
    fields[19] = "500"
    fields[20] = "2048"
    fields[21] = "64"

    mock_read_text.return_value = (
        "123 (my python process) " + " ".join(fields)
    )

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is True
    assert "state: R" in result.output
    assert "threads: 2" in result.output
    assert "start_time: 500" in result.output
    assert "virtual_memory: 2048" in result.output
    assert "resident_pages: 64" in result.output


@patch("tony.tools.process.stats.Path.read_text")
def test_process_not_found(mock_read_text) -> None:
    mock_read_text.side_effect = FileNotFoundError

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="999999")]
    )

    assert result.success is False
    assert result.error == "Process '999999' was not found."


@patch("tony.tools.process.stats.Path.read_text")
def test_permission_denied(mock_read_text) -> None:
    mock_read_text.side_effect = PermissionError

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == (
        "Permission denied reading statistics of process '123'."
    )


@patch("tony.tools.process.stats.Path.read_text")
def test_os_error(mock_read_text) -> None:
    mock_read_text.side_effect = OSError("proc unavailable")

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert result.error == "proc unavailable"


@patch("tony.tools.process.stats.Path.read_text")
def test_malformed_stat(mock_read_text) -> None:
    mock_read_text.return_value = "123 (python)"

    result = ProcessStatsTool().execute(
        [ToolArgument(name="pid", value="123")]
    )

    assert result.success is False
    assert (
        result.error
        == "Process statistics are unavailable for process '123'."
    )


def test_parse_stat_missing_closing_parenthesis() -> None:
    result = ProcessStatsTool._parse_stat(
        "123 (python process"
    )

    assert result is None


def test_parse_stat_empty_remainder() -> None:
    result = ProcessStatsTool._parse_stat(
        "123 (python process)"
    )

    assert result is None

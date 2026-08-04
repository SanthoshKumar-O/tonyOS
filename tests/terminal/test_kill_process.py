"""Tests for KillProcessTool."""

from __future__ import annotations

from tony.tools.terminal import KillProcessTool


def test_metadata() -> None:
    tool = KillProcessTool()

    assert tool.metadata.name == "kill_process"


def test_requires_pid() -> None:
    tool = KillProcessTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Process ID is required."

"""Tests for MemoryUsageTool."""

from __future__ import annotations

from tony.tools.terminal import MemoryUsageTool


def test_metadata() -> None:
    tool = MemoryUsageTool()

    assert tool.metadata.name == "memory_usage"


def test_execute() -> None:
    tool = MemoryUsageTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

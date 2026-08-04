"""Tests for DiskUsageTool."""

from __future__ import annotations

from tony.tools.terminal import DiskUsageTool


def test_metadata() -> None:
    tool = DiskUsageTool()

    assert tool.metadata.name == "disk_usage"


def test_execute() -> None:
    tool = DiskUsageTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

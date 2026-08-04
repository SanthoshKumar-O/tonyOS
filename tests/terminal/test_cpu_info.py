"""Tests for CpuInfoTool."""

from __future__ import annotations

from tony.tools.terminal import CpuInfoTool


def test_metadata() -> None:
    tool = CpuInfoTool()

    assert tool.metadata.name == "cpu_info"


def test_execute() -> None:
    tool = CpuInfoTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

"""Tests for PackageListTool."""

from __future__ import annotations

from tony.tools.package import PackageListTool


def test_metadata() -> None:
    tool = PackageListTool()

    assert tool.metadata.name == "package_list"
    assert tool.metadata.capability.value == "shell"


def test_execute_returns_tool_result() -> None:
    tool = PackageListTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

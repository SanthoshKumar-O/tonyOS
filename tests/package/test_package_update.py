"""Tests for PackageUpdateTool."""

from __future__ import annotations

from tony.tools.package import PackageUpdateTool


def test_metadata() -> None:
    tool = PackageUpdateTool()

    assert tool.metadata.name == "package_update"
    assert tool.metadata.capability.value == "shell"


def test_execute_returns_result() -> None:
    tool = PackageUpdateTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

"""Tests for PackageRemoveTool."""

from __future__ import annotations

from tony.tools.package import PackageRemoveTool


def test_metadata() -> None:
    tool = PackageRemoveTool()

    assert tool.metadata.name == "package_remove"
    assert tool.metadata.capability.value == "shell"


def test_requires_package_name() -> None:
    tool = PackageRemoveTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Package name is required."

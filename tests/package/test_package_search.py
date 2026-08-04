"""Tests for PackageSearchTool."""

from __future__ import annotations

from tony.tools.package import PackageSearchTool


def test_metadata() -> None:
    tool = PackageSearchTool()

    assert tool.metadata.name == "package_search"
    assert tool.metadata.capability.value == "shell"


def test_requires_search_term() -> None:
    tool = PackageSearchTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Search term is required."

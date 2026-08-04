"""Tests for the package registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.package import PackageRegistry


def test_package_registry_registers() -> None:
    registry = ToolRegistry()

    PackageRegistry.register(registry)

    assert registry is not None
    assert registry.get("package_install").metadata.name == "package_install"
    assert registry.get("package_remove").metadata.name == "package_remove"
    assert registry.get("package_update").metadata.name == "package_update"
    assert registry.get("package_search").metadata.name == "package_search"
    assert registry.get("package_list").metadata.name == "package_list"

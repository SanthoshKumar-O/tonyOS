"""Tests for PackageInstallTool."""

from __future__ import annotations

from tony.tools.package import PackageInstallTool


def test_metadata() -> None:
    tool = PackageInstallTool()

    assert tool.metadata.name == "package_install"
    assert tool.metadata.capability.value == "shell"


def test_requires_package_name() -> None:
    tool = PackageInstallTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Package name is required."

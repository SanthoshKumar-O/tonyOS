"""Tests for PythonInstallTool."""

from __future__ import annotations

from tony.tools.python import PythonInstallTool


def test_metadata() -> None:
    tool = PythonInstallTool()

    assert tool.metadata.name == "python_install"
    assert tool.metadata.capability.value == "python"


def test_requires_package_name() -> None:
    tool = PythonInstallTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Package name is required."

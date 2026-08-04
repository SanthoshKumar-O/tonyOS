"""Tests for the Python registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.python import PythonRegistry


def test_python_registry_registers() -> None:
    registry = ToolRegistry()

    PythonRegistry.register(registry)

    assert registry is not None
    assert registry.get("python_execute").metadata.name == "python_execute"
    assert registry.get("python_run").metadata.name == "python_run"
    assert registry.get("python_venv").metadata.name == "python_venv"
    assert registry.get("python_install").metadata.name == "python_install"
    assert registry.get("python_list").metadata.name == "python_list"
    assert registry.get("python_freeze").metadata.name == "python_freeze"

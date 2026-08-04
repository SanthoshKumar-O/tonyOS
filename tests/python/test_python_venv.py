"""Tests for PythonVenvTool."""

from __future__ import annotations

from tony.tools.python import PythonVenvTool


def test_metadata() -> None:
    tool = PythonVenvTool()

    assert tool.metadata.name == "python_venv"
    assert tool.metadata.capability.value == "python"


def test_requires_venv_name() -> None:
    tool = PythonVenvTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Virtual environment name is required."

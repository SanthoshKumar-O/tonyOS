"""Tests for PythonExecuteTool."""

from __future__ import annotations

from tony.tools.python import PythonExecuteTool


def test_metadata() -> None:
    tool = PythonExecuteTool()

    assert tool.metadata.name == "python_execute"
    assert tool.metadata.capability.value == "python"


def test_requires_script_path() -> None:
    tool = PythonExecuteTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Python script path is required."

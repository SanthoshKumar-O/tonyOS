"""Tests for PythonRunTool."""

from __future__ import annotations

from tony.tools.python import PythonRunTool


def test_metadata() -> None:
    tool = PythonRunTool()

    assert tool.metadata.name == "python_run"
    assert tool.metadata.capability.value == "python"


def test_requires_code() -> None:
    tool = PythonRunTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Python code is required."

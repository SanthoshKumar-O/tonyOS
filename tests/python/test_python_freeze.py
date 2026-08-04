"""Tests for PythonFreezeTool."""

from __future__ import annotations

from tony.tools.python import PythonFreezeTool


def test_metadata() -> None:
    tool = PythonFreezeTool()

    assert tool.metadata.name == "python_freeze"
    assert tool.metadata.capability.value == "python"


def test_execute_returns_result() -> None:
    tool = PythonFreezeTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

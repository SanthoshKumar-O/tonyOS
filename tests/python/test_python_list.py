"""Tests for PythonListTool."""

from __future__ import annotations

from tony.tools.python import PythonListTool


def test_metadata() -> None:
    tool = PythonListTool()

    assert tool.metadata.name == "python_list"
    assert tool.metadata.capability.value == "python"


def test_execute_returns_result() -> None:
    tool = PythonListTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

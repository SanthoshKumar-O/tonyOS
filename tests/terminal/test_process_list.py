"""Tests for ProcessListTool."""

from __future__ import annotations

from tony.tools.terminal import ProcessListTool


def test_metadata() -> None:
    tool = ProcessListTool()

    assert tool.metadata.name == "process_list"


def test_execute() -> None:
    tool = ProcessListTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

"""Tests for DateTool."""

from __future__ import annotations

from tony.tools.terminal import DateTool


def test_metadata() -> None:
    tool = DateTool()

    assert tool.metadata.name == "date"


def test_execute() -> None:
    tool = DateTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

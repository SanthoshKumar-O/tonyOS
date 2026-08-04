"""Tests for UnameTool."""

from __future__ import annotations

from tony.tools.terminal import UnameTool


def test_metadata() -> None:
    tool = UnameTool()

    assert tool.metadata.name == "uname"


def test_execute() -> None:
    tool = UnameTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

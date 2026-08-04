"""Tests for UptimeTool."""

from __future__ import annotations

from tony.tools.terminal import UptimeTool


def test_metadata() -> None:
    tool = UptimeTool()

    assert tool.metadata.name == "uptime"


def test_execute() -> None:
    tool = UptimeTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

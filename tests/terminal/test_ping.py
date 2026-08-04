"""Tests for PingTool."""

from __future__ import annotations

from tony.tools.terminal import PingTool


def test_metadata() -> None:
    tool = PingTool()

    assert tool.metadata.name == "ping"


def test_requires_host() -> None:
    tool = PingTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Host is required."

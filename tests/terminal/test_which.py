"""Tests for WhichTool."""

from __future__ import annotations

from tony.tools.terminal import WhichTool


def test_metadata() -> None:
    tool = WhichTool()

    assert tool.metadata.name == "which"


def test_requires_command() -> None:
    tool = WhichTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Command name is required."

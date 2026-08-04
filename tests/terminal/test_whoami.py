"""Tests for WhoAmITool."""

from __future__ import annotations

from tony.tools.terminal import WhoAmITool


def test_metadata() -> None:
    tool = WhoAmITool()

    assert tool.metadata.name == "whoami"


def test_execute() -> None:
    tool = WhoAmITool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

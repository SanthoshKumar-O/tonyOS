"""Tests for HostnameTool."""

from __future__ import annotations

from tony.tools.terminal import HostnameTool


def test_metadata() -> None:
    tool = HostnameTool()

    assert tool.metadata.name == "hostname"


def test_execute() -> None:
    tool = HostnameTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

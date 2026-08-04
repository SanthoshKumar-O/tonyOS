"""Tests for OsInfoTool."""

from __future__ import annotations

from tony.tools.terminal import OsInfoTool


def test_metadata() -> None:
    tool = OsInfoTool()

    assert tool.metadata.name == "os_info"


def test_execute() -> None:
    tool = OsInfoTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

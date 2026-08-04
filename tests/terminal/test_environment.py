"""Tests for EnvironmentTool."""

from __future__ import annotations

from tony.tools.terminal import EnvironmentTool


def test_metadata() -> None:
    tool = EnvironmentTool()

    assert tool.metadata.name == "environment"


def test_execute() -> None:
    tool = EnvironmentTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

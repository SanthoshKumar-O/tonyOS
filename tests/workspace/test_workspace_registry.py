"""Tests for the Workspace tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.workspace import register_workspace_tools


def test_registers_all_workspace_tools() -> None:
    registry = ToolRegistry()

    register_workspace_tools(registry)

    assert registry.exists("workspace_root")
    assert registry.exists("project_detect")
    assert registry.exists("workspace_info")
    assert registry.exists("workspace_list")


def test_registers_exactly_four_workspace_tools() -> None:
    registry = ToolRegistry()

    register_workspace_tools(registry)

    assert len(registry.tools()) == 4
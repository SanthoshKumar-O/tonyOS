"""Tests for the Git registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.git import GitRegistry


def test_git_registry_registers() -> None:
    registry = ToolRegistry()

    GitRegistry.register(registry)

    tool = registry.get("git_init")

    assert tool.metadata.name == "git_init"
    assert registry.get("git_status").metadata.name == "git_status"
    assert registry.get("git_add").metadata.name == "git_add"
    assert registry.get("git_commit").metadata.name == "git_commit"
    assert registry.get("git_branch").metadata.name == "git_branch"
    assert registry.get("git_checkout").metadata.name == "git_checkout"
    assert registry.get("git_log").metadata.name == "git_log"
    assert registry.get("git_diff").metadata.name == "git_diff"
    assert registry.get("git_clone").metadata.name == "git_clone"

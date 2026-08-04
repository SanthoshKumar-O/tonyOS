"""Tests for GitCloneTool."""

from __future__ import annotations

from tony.tools.git import GitCloneTool


def test_metadata() -> None:
    tool = GitCloneTool()

    assert tool.metadata.name == "git_clone"
    assert tool.metadata.capability.value == "git"


def test_git_clone_requires_arguments() -> None:
    tool = GitCloneTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == ("Repository URL and destination are required.")

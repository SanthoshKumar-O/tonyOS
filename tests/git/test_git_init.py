"""Tests for GitInitTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import GitInitTool


def test_metadata() -> None:
    tool = GitInitTool()

    assert tool.metadata.name == "git_init"
    assert tool.metadata.capability.value == "git"


def test_git_init(
    tmp_path: Path,
) -> None:
    tool = GitInitTool()

    repo = tmp_path / "repo"

    result = tool.execute(
        [
            ToolArgument(
                name="directory",
                value=str(repo),
            ),
        ],
    )

    assert result.success is True
    assert (repo / ".git").exists()

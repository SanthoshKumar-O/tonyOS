"""Tests for GitStatusTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitInitTool,
    GitStatusTool,
)


def test_metadata() -> None:
    tool = GitStatusTool()

    assert tool.metadata.name == "git_status"
    assert tool.metadata.capability.value == "git"


def test_git_status(
    tmp_path: Path,
) -> None:
    init_tool = GitInitTool()

    repo = tmp_path / "repo"

    init_tool.execute(
        [
            ToolArgument(
                name="directory",
                value=str(repo),
            ),
        ],
    )

    tool = GitStatusTool()

    result = tool.execute(
        [
            ToolArgument(
                name="directory",
                value=str(repo),
            ),
        ],
    )

    assert result.success is True
    assert "On branch" in result.output

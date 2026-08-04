"""Tests for GitAddTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitAddTool,
    GitInitTool,
)


def test_metadata() -> None:
    tool = GitAddTool()

    assert tool.metadata.name == "git_add"
    assert tool.metadata.capability.value == "git"


def test_git_add(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"

    GitInitTool().execute(
        [
            ToolArgument(
                name="directory",
                value=str(repo),
            ),
        ],
    )

    file = repo / "README.md"
    file.write_text(
        "Tony",
        encoding="utf-8",
    )

    tool = GitAddTool()

    result = tool.execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
            ToolArgument(
                name="file",
                value="README.md",
            ),
        ],
    )

    assert result.success is True

"""Tests for GitDiffTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitDiffTool,
    GitInitTool,
)


def test_metadata() -> None:
    tool = GitDiffTool()

    assert tool.metadata.name == "git_diff"
    assert tool.metadata.capability.value == "git"


def test_git_diff(
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
        "Version 1",
        encoding="utf-8",
    )

    file.write_text(
        "Version 2",
        encoding="utf-8",
    )

    result = GitDiffTool().execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
        ],
    )

    assert result.success is True

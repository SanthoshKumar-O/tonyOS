"""Tests for GitCommitTool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitAddTool,
    GitCommitTool,
    GitInitTool,
)


def test_metadata() -> None:
    tool = GitCommitTool()

    assert tool.metadata.name == "git_commit"
    assert tool.metadata.capability.value == "git"


def test_git_commit(
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

    subprocess.run(
        ["git", "-C", str(repo), "config", "user.name", "Tony"],
        check=True,
    )

    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "tony@example.com"],
        check=True,
    )

    file = repo / "README.md"
    file.write_text(
        "Tony",
        encoding="utf-8",
    )

    GitAddTool().execute(
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

    result = GitCommitTool().execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
            ToolArgument(
                name="message",
                value="Initial commit",
            ),
        ],
    )

    assert result.success is True

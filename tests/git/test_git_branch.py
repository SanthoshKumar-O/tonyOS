"""Tests for GitBranchTool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitAddTool,
    GitBranchTool,
    GitCommitTool,
    GitInitTool,
)


def test_metadata() -> None:
    tool = GitBranchTool()

    assert tool.metadata.name == "git_branch"
    assert tool.metadata.capability.value == "git"


def test_git_branch(
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

    readme = repo / "README.md"

    readme.write_text(
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

    GitCommitTool().execute(
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

    result = GitBranchTool().execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
        ],
    )

    assert result.success is True
    assert "main" in result.output or "master" in result.output

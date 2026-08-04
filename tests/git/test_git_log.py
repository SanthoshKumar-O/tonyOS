"""Tests for GitLogTool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitAddTool,
    GitCommitTool,
    GitInitTool,
    GitLogTool,
)


def test_metadata() -> None:
    tool = GitLogTool()

    assert tool.metadata.name == "git_log"
    assert tool.metadata.capability.value == "git"


def test_git_log(
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

    (repo / "README.md").write_text(
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

    result = GitLogTool().execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
        ],
    )

    assert result.success is True
    assert "Initial commit" in result.output

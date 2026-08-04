"""Tests for GitCheckoutTool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.git import (
    GitAddTool,
    GitCheckoutTool,
    GitCommitTool,
    GitInitTool,
)


def test_metadata() -> None:
    tool = GitCheckoutTool()

    assert tool.metadata.name == "git_checkout"
    assert tool.metadata.capability.value == "git"


def test_git_checkout(
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

    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "branch",
            "feature",
        ],
        check=True,
    )

    result = GitCheckoutTool().execute(
        [
            ToolArgument(
                name="repository",
                value=str(repo),
            ),
            ToolArgument(
                name="branch",
                value="feature",
            ),
        ],
    )

    assert result.success is True

"""Git commit tool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseGitTool


class GitCommitTool(BaseGitTool):
    """Creates a Git commit."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_commit",
            description="Create a Git commit.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git commit."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Repository path and commit message are required.",
            )

        repository = Path(arguments[0].value)
        message = arguments[1].value

        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "commit",
                "-m",
                message,
            ],
            capture_output=True,
            text=True,
            timeout=self._TIMEOUT,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )

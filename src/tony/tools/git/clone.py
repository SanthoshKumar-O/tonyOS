"""Git clone tool."""

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


class GitCloneTool(BaseGitTool):
    """Clones a Git repository."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_clone",
            description="Clone a Git repository.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git clone."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Repository URL and destination are required.",
            )

        repository = arguments[0].value
        destination = Path(arguments[1].value)

        result = subprocess.run(
            [
                "git",
                "clone",
                repository,
                str(destination),
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

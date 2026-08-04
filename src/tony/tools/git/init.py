"""Git init tool."""

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


class GitInitTool(BaseGitTool):
    """Initializes a Git repository."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_init",
            description="Initialize a Git repository.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git init."""

        directory = Path(arguments[0].value) if arguments else Path.cwd()

        result = subprocess.run(
            [
                "git",
                "init",
                str(directory),
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

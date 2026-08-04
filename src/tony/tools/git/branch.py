"""Git branch tool."""

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


class GitBranchTool(BaseGitTool):
    """Lists Git branches."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_branch",
            description="List Git branches.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git branch."""

        repository = Path(arguments[0].value) if arguments else Path.cwd()

        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "branch",
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

"""Git log tool."""

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


class GitLogTool(BaseGitTool):
    """Displays Git commit history."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_log",
            description="Show Git commit history.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git log."""

        repository = Path(arguments[0].value) if arguments else Path.cwd()

        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "log",
                "--oneline",
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

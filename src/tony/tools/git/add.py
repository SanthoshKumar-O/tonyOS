"""Git add tool."""

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


class GitAddTool(BaseGitTool):
    """Stages files in a Git repository."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="git_add",
            description="Stage files in a Git repository.",
            capability=ToolCapability.GIT,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute git add."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Repository path and file path are required.",
            )

        repository = Path(arguments[0].value)
        file_path = arguments[1].value

        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "add",
                file_path,
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

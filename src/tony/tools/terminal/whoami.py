"""WhoAmI tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class WhoAmITool(BaseTerminalTool):
    """Returns the current user."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="whoami",
            description="Show the current user.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute whoami."""

        result = subprocess.run(
            [
                "whoami",
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

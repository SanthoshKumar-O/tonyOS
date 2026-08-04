"""Which tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class WhichTool(BaseTerminalTool):
    """Locate a command."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="which",
            description="Locate a command.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute which."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Command name is required.",
            )

        result = subprocess.run(
            [
                "which",
                arguments[0].value,
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

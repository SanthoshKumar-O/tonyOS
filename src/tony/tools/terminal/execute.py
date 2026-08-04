"""Execute command tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class ExecuteCommandTool(BaseTerminalTool):
    """Execute arbitrary shell commands."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="execute",
            description="Execute a shell command.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute a shell command."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Command is required.",
            )

        command = [argument.value for argument in arguments]

        result = subprocess.run(
            command,
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

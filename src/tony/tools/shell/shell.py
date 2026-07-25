"""Shell command execution tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)
from tony.tools.filesystem.base import BaseFilesystemTool


class ShellTool(BaseFilesystemTool):
    """Executes shell commands."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="shell",
            description="Execute shell commands.",
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
                error="A command is required.",
            )

        command = [argument.value for argument in arguments]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output="",
                error="Command execution timed out.",
                exit_code=124,
            )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout,
            error=result.stderr,
            exit_code=result.returncode,
        )

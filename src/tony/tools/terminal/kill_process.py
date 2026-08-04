"""Kill process tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class KillProcessTool(BaseTerminalTool):
    """Kill a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="kill_process",
            description="Kill a running process.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute kill."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Process ID is required.",
            )

        pid = arguments[0].value

        result = subprocess.run(
            [
                "kill",
                pid,
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

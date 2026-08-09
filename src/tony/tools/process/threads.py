"""Process thread inspection tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessThreadsTool(BaseProcessTool):
    """Show threads belonging to a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_threads",
            description="Show threads belonging to a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Show process threads."""

        if not arguments:
            return ToolResult(
                success=False,
                error="Process ID is required.",
            )

        pid = arguments[0].value.strip()

        if not pid:
            return ToolResult(
                success=False,
                error="Process ID cannot be empty.",
            )

        if not pid.isdigit() or int(pid) <= 0:
            return ToolResult(
                success=False,
                error="Process ID must be a positive integer.",
            )

        try:
            result = subprocess.run(
                [
                    "ps",
                    "-T",
                    "-p",
                    pid,
                    "-o",
                    "pid=,spid=,pcpu=,stat=,comm=",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if result.returncode != 0 or not result.stdout.strip():
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
                exit_code=result.returncode,
            )

        return ToolResult(
            success=True,
            output=result.stdout.strip(),
            exit_code=0,
        )
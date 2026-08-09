"""Process inspection tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class InspectProcessTool(BaseProcessTool):
    """Inspect detailed information about a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="inspect_process",
            description="Show detailed information about a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Inspect a process by PID."""

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

        if not pid.isdigit():
            return ToolResult(
                success=False,
                error="Process ID must be a positive integer.",
            )

        if int(pid) <= 0:
            return ToolResult(
                success=False,
                error="Process ID must be a positive integer.",
            )

        try:
            result = subprocess.run(
                [
                    "ps",
                    "-p",
                    pid,
                    "-o",
                    "pid=,ppid=,user=,stat=,etime=,cmd=",
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
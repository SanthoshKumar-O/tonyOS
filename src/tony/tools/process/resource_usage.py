"""Process resource usage tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessResourceUsageTool(BaseProcessTool):
    """Show CPU and memory usage for a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_resource_usage",
            description="Show CPU and memory usage for a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Show resource usage for a process."""

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
                    "-p",
                    pid,
                    "-o",
                    "pid=,pcpu=,pmem=,rss=,vsz=,etime=,cmd=",
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
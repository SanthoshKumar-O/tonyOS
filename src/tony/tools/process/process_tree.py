"""Process tree tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessTreeTool(BaseProcessTool):
    """Display the process hierarchy."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_tree",
            description="Display the running process hierarchy.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Display the process tree."""

        command = [
            "ps",
            "-eo",
            "pid=,ppid=,user=,stat=,cmd=",
            "--forest",
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if result.returncode != 0:
            return ToolResult(
                success=False,
                error=result.stderr.strip()
                or "Failed to retrieve process tree.",
                exit_code=result.returncode,
            )

        return ToolResult(
            success=True,
            output=result.stdout.strip(),
            exit_code=0,
        )
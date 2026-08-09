"""Process priority tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class SetProcessPriorityTool(BaseProcessTool):
    """Change the nice value of a running process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="set_process_priority",
            description="Change the scheduling priority of a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Change a process nice value."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                error="Process ID and priority are required.",
            )

        pid = arguments[0].value.strip()
        priority = arguments[1].value.strip()

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
            nice_value = int(priority)
        except ValueError:
            return ToolResult(
                success=False,
                error="Priority must be an integer.",
            )

        if not -20 <= nice_value <= 19:
            return ToolResult(
                success=False,
                error="Priority must be between -20 and 19.",
            )

        try:
            result = subprocess.run(
                [
                    "renice",
                    str(nice_value),
                    "-p",
                    pid,
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

        if result.returncode != 0:
            return ToolResult(
                success=False,
                error=result.stderr.strip()
                or f"Failed to change priority of process '{pid}'.",
                exit_code=result.returncode,
            )

        return ToolResult(
            success=True,
            output=result.stdout.strip(),
            exit_code=0,
        )
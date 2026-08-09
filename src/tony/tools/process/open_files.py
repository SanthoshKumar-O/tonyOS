"""Process open files tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessOpenFilesTool(BaseProcessTool):
    """Show files currently opened by a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_open_files",
            description="Show files currently opened by a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Show open files for a process."""

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
                    "lsof",
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
                or f"Failed to inspect open files for process '{pid}'.",
                exit_code=result.returncode,
            )

        return ToolResult(
            success=True,
            output=result.stdout.strip(),
            exit_code=0,
        )
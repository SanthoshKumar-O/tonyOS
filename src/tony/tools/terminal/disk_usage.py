"""Disk usage tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class DiskUsageTool(BaseTerminalTool):
    """Displays disk usage."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="disk_usage",
            description="Show disk usage.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute df."""

        result = subprocess.run(
            [
                "df",
                "-h",
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

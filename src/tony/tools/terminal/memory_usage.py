"""Memory usage tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class MemoryUsageTool(BaseTerminalTool):
    """Displays memory usage."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="memory_usage",
            description="Show memory usage.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute free."""

        result = subprocess.run(
            [
                "free",
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

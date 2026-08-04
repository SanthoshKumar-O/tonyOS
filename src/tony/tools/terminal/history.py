"""History tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class HistoryTool(BaseTerminalTool):
    """Displays shell history."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="history",
            description="Show shell history.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute history."""

        result = subprocess.run(
            [
                "bash",
                "-c",
                "history",
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

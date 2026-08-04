"""Uptime tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class UptimeTool(BaseTerminalTool):
    """Displays system uptime."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="uptime",
            description="Show system uptime.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute uptime."""

        result = subprocess.run(
            ["uptime"],
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

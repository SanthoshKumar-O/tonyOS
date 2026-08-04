"""Hostname tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class HostnameTool(BaseTerminalTool):
    """Returns the system hostname."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="hostname",
            description="Show the system hostname.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute hostname."""

        result = subprocess.run(
            [
                "hostname",
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

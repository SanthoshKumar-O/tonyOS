"""Ping tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class PingTool(BaseTerminalTool):
    """Ping a host."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="ping",
            description="Ping a network host.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute ping."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Host is required.",
            )

        result = subprocess.run(
            [
                "ping",
                "-c",
                "4",
                arguments[0].value,
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

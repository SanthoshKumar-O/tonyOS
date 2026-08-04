"""IP address tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class IpAddressTool(BaseTerminalTool):
    """Displays IP addresses."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="ip_address",
            description="Show IP addresses.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute ip addr."""

        result = subprocess.run(
            [
                "ip",
                "addr",
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

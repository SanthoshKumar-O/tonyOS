"""Network interfaces tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class NetworkInterfacesTool(BaseTerminalTool):
    """Displays network interfaces."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="network_interfaces",
            description="Show network interfaces.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute ip link."""

        result = subprocess.run(
            [
                "ip",
                "link",
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

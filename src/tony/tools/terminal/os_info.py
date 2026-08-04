"""OS information tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class OsInfoTool(BaseTerminalTool):
    """Displays operating system information."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="os_info",
            description="Show operating system information.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute hostnamectl."""

        result = subprocess.run(
            [
                "hostnamectl",
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

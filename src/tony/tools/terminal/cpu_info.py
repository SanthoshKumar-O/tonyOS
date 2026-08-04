"""CPU info tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class CpuInfoTool(BaseTerminalTool):
    """Displays CPU information."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="cpu_info",
            description="Show CPU information.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute lscpu."""

        result = subprocess.run(
            [
                "lscpu",
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

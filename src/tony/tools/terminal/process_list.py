"""Process list tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class ProcessListTool(BaseTerminalTool):
    """List running processes."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_list",
            description="List running processes.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute ps."""

        result = subprocess.run(
            [
                "ps",
                "-ef",
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

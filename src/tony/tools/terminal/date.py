"""Date tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class DateTool(BaseTerminalTool):
    """Displays the current system date and time."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="date",
            description="Show the current date and time.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute date."""

        result = subprocess.run(
            ["date"],
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

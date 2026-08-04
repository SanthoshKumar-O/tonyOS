"""Uname tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseTerminalTool


class UnameTool(BaseTerminalTool):
    """Returns kernel information."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="uname",
            description="Show kernel information.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute uname."""

        result = subprocess.run(
            [
                "uname",
                "-a",
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

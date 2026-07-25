"""Print working directory tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class PwdTool(BaseFilesystemTool):
    """Returns the current working directory."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="pwd",
            description="Print the current working directory.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the pwd tool."""

        directory = Path.cwd()

        return ToolResult(
            success=True,
            output=str(directory),
        )

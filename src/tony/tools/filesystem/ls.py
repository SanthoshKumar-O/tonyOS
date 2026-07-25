"""List directory contents tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class LsTool(BaseFilesystemTool):
    """Lists the contents of a directory."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="ls",
            description="List directory contents.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the ls tool."""

        directory = Path(arguments[0].value) if arguments else Path.cwd()
        entries = sorted(path.name for path in directory.iterdir())

        return ToolResult(
            success=True,
            output="\n".join(entries),
        )

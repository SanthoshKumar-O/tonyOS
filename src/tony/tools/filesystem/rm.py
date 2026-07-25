"""Remove file tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class RmTool(BaseFilesystemTool):
    """Removes a file."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="rm",
            description="Remove a file.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the rm tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="A file path is required.",
            )

        file_path = Path(arguments[0].value)

        file_path.unlink()

        return ToolResult(
            success=True,
            output=str(file_path),
        )

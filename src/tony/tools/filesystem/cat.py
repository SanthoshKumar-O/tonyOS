"""Read file contents tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class CatTool(BaseFilesystemTool):
    """Reads the contents of a text file."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="cat",
            description="Read the contents of a text file.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the cat tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="A file path is required.",
            )

        file_path = Path(arguments[0].value)

        content = file_path.read_text(
            encoding="utf-8",
        )

        return ToolResult(
            success=True,
            output=content,
        )

"""Touch file tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class TouchTool(BaseFilesystemTool):
    """Creates an empty file or updates its modification time."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="touch",
            description="Create an empty file.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the touch tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="A file path is required.",
            )

        file_path = Path(arguments[0].value)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path.touch(
            exist_ok=True,
        )

        return ToolResult(
            success=True,
            output=str(file_path),
        )

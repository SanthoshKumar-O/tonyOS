"""Create directory tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class MkdirTool(BaseFilesystemTool):
    """Creates a directory."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="mkdir",
            description="Create a directory.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the mkdir tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="A directory path is required.",
            )

        directory = Path(arguments[0].value)

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return ToolResult(
            success=True,
            output=str(directory),
        )

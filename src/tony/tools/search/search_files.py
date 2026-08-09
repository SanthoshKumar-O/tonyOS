"""File search tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseSearchTool


class SearchFilesTool(BaseSearchTool):
    """Find files matching a pattern."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="search_files",
            description="Find files in the current workspace matching a pattern.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Search for files."""

        if not arguments:
            return ToolResult(
                success=False,
                error="Search pattern is required.",
            )

        pattern = arguments[0].value.strip()

        if not pattern:
            return ToolResult(
                success=False,
                error="Search pattern cannot be empty.",
            )

        root = Path.cwd().resolve()

        try:
            matches = sorted(
                path
                for path in root.rglob(pattern)
                if path.is_file()
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not matches:
            return ToolResult(
                success=True,
                output="No matching files found.",
            )

        output = "\n".join(
            str(path.relative_to(root))
            for path in matches
        )

        return ToolResult(
            success=True,
            output=output,
        )
"""Directory search tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseSearchTool


class SearchDirectoryTool(BaseSearchTool):
    """Find directories matching a pattern."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="search_directory",
            description="Find directories in the current workspace matching a pattern.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Search for directories."""

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
                if path.is_dir()
                and ".git" not in path.parts
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not matches:
            return ToolResult(
                success=True,
                output="No matching directories found.",
            )

        output = "\n".join(
            str(path.relative_to(root))
            for path in matches
        )

        return ToolResult(
            success=True,
            output=output,
        )
"""Text search tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseSearchTool


class SearchTextTool(BaseSearchTool):
    """Search file contents for text."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="search_text",
            description="Search file contents in the current workspace.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Search file contents."""

        if not arguments:
            return ToolResult(
                success=False,
                error="Search text is required.",
            )

        pattern = arguments[0].value

        if not pattern:
            return ToolResult(
                success=False,
                error="Search text cannot be empty.",
            )

        root = Path.cwd().resolve()
        matches: list[str] = []

        try:
            for path in root.rglob("*"):
                if not path.is_file():
                    continue

                if ".git" in path.parts:
                    continue

                try:
                    content = path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                except (OSError, UnicodeError):
                    continue

                for line_number, line in enumerate(
                    content.splitlines(),
                    start=1,
                ):
                    if pattern in line:
                        relative = path.relative_to(root)
                        matches.append(
                            f"{relative}:{line_number}:{line}"
                        )

        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not matches:
            return ToolResult(
                success=True,
                output="No matching text found.",
            )

        return ToolResult(
            success=True,
            output="\n".join(matches),
        )
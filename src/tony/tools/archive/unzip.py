"""Unzip archive tool."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseArchiveTool


class UnzipTool(BaseArchiveTool):
    """Extracts a ZIP archive."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="unzip",
            description="Extract a ZIP archive.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the unzip tool."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Source and destination paths are required.",
            )

        source = Path(arguments[0].value)
        destination = Path(arguments[1].value)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        with ZipFile(source) as archive:
            destination = destination.resolve()

            for member in archive.infolist():
                member_path = (destination / member.filename).resolve()

                if member_path != destination and destination not in member_path.parents:
                    return ToolResult(
                        success=False,
                        output="",
                        error="Archive contains an unsafe path.",
                    )

            archive.extractall(destination)

        return ToolResult(
            success=True,
            output=str(destination),
        )

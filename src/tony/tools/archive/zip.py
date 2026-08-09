"""ZIP archive tool."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseArchiveTool


class ZipTool(BaseArchiveTool):
    """Creates a ZIP archive."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="zip",
            description="Create a ZIP archive.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the zip tool."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Source and destination paths are required.",
            )

        source = Path(arguments[0].value)
        destination = Path(arguments[1].value)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with ZipFile(
            destination,
            mode="w",
            compression=ZIP_DEFLATED,
        ) as archive:
            if source.is_dir():
                for path in source.rglob("*"):
                    if path.is_file():
                        archive.write(
                            path,
                            path.relative_to(source.parent),
                        )
            else:
                archive.write(
                    source,
                    source.name,
                )

        return ToolResult(
            success=True,
            output=str(destination),
        )

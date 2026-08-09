"""TAR archive tool."""

from __future__ import annotations

import tarfile
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseArchiveTool


class TarTool(BaseArchiveTool):
    """Creates a TAR archive."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="tar",
            description="Create a TAR archive.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the tar tool."""

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

        with tarfile.open(
            destination,
            mode="w",
        ) as archive:
            archive.add(
                source,
                arcname=source.name,
            )

        return ToolResult(
            success=True,
            output=str(destination),
        )

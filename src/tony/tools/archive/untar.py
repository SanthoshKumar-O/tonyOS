"""Untar archive tool."""

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


class UntarTool(BaseArchiveTool):
    """Extracts a TAR archive."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="untar",
            description="Extract a TAR archive.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the untar tool."""

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

        destination = destination.resolve()

        with tarfile.open(source) as archive:
            for member in archive.getmembers():
                member_path = (destination / member.name).resolve()

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

"""Move file tool."""

from __future__ import annotations

import shutil
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseFilesystemTool


class MvTool(BaseFilesystemTool):
    """Moves a file."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="mv",
            description="Move a file.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the mv tool."""

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

        shutil.move(
            str(source),
            str(destination),
        )

        return ToolResult(
            success=True,
            output=str(destination),
        )

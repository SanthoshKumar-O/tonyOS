"""Thumbnail generation tool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseMediaTool


class ThumbnailTool(BaseMediaTool):
    """Generates a thumbnail from an image."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="thumbnail",
            description="Generate a thumbnail from an image.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the thumbnail tool."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                output="",
                error="Source and destination paths are required.",
            )

        source = Path(arguments[0].value)
        destination = Path(arguments[1].value)

        if not source.exists():
            return ToolResult(
                success=False,
                output="",
                error="Source file does not exist.",
            )

        if not source.is_file():
            return ToolResult(
                success=False,
                output="",
                error="Source path must be a file.",
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        result = subprocess.run(
            [
                "magick",
                str(source),
                "-thumbnail",
                "200x200",
                str(destination),
            ],
            capture_output=True,
            text=True,
            timeout=self._TIMEOUT,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=str(destination) if result.returncode == 0 else "",
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )
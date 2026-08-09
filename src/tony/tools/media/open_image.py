"""Open image tool."""

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


class OpenImageTool(BaseMediaTool):
    """Opens an image using the system default application."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="open_image",
            description="Open an image using the system default application.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the open_image tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="An image path is required.",
            )

        image_path = Path(arguments[0].value)

        if not image_path.exists():
            return ToolResult(
                success=False,
                output="",
                error="Image file does not exist.",
            )

        if not image_path.is_file():
            return ToolResult(
                success=False,
                output="",
                error="Image path must be a file.",
            )

        result = subprocess.run(
            [
                "xdg-open",
                str(image_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )
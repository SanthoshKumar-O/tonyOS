"""Play audio tool."""

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


class PlayAudioTool(BaseMediaTool):
    """Plays an audio file using the system default application."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="play_audio",
            description="Play an audio file using the system default application.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the play_audio tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="An audio path is required.",
            )

        audio_path = Path(arguments[0].value)

        if not audio_path.exists():
            return ToolResult(
                success=False,
                output="",
                error="Audio file does not exist.",
            )

        if not audio_path.is_file():
            return ToolResult(
                success=False,
                output="",
                error="Audio path must be a file.",
            )

        result = subprocess.run(
            [
                "xdg-open",
                str(audio_path),
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
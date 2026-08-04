"""Docker ps tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseDockerTool


class DockerPsTool(BaseDockerTool):
    """Lists running Docker containers."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="docker_ps",
            description="List running Docker containers.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute docker ps."""

        result = subprocess.run(
            [
                "docker",
                "ps",
            ],
            capture_output=True,
            text=True,
            timeout=self._TIMEOUT,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )

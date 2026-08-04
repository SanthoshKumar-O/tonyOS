"""Docker pull tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseDockerTool


class DockerPullTool(BaseDockerTool):
    """Pulls a Docker image."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="docker_pull",
            description="Pull a Docker image.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute docker pull."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Docker image name is required.",
            )

        image = arguments[0].value

        result = subprocess.run(
            [
                "docker",
                "pull",
                image,
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

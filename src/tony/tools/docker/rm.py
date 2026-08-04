"""Docker rm tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseDockerTool


class DockerRmTool(BaseDockerTool):
    """Removes a Docker container."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="docker_rm",
            description="Remove a Docker container.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute docker rm."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Container name or ID is required.",
            )

        container = arguments[0].value

        result = subprocess.run(
            [
                "docker",
                "rm",
                container,
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

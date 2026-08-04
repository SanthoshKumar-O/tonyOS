"""Docker run tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseDockerTool


class DockerRunTool(BaseDockerTool):
    """Runs a Docker container."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="docker_run",
            description="Run a Docker container.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute docker run."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Docker image name is required.",
            )

        command = [
            "docker",
            "run",
        ]

        command.extend(argument.value for argument in arguments)

        result = subprocess.run(
            command,
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

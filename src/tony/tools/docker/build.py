"""Docker build tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseDockerTool


class DockerBuildTool(BaseDockerTool):
    """Builds a Docker image."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="docker_build",
            description="Build a Docker image.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute docker build."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Build context is required.",
            )

        command = [
            "docker",
            "build",
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

"""Package remove tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePackageTool


class PackageRemoveTool(BasePackageTool):
    """Removes packages using DNF."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="package_remove",
            description="Remove a package using DNF.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute dnf remove."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Package name is required.",
            )

        package = arguments[0].value

        result = subprocess.run(
            [
                "sudo",
                "dnf5",
                "remove",
                "-y",
                package,
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

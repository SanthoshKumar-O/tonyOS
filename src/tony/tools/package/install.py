"""Package install tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePackageTool


class PackageInstallTool(BasePackageTool):
    """Installs packages using DNF."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="package_install",
            description="Install a package using DNF.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute dnf install."""

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
                "dnf",
                "install",
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

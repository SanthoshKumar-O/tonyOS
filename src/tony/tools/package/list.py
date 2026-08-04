"""Package list tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePackageTool


class PackageListTool(BasePackageTool):
    """Lists installed packages using DNF."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="package_list",
            description="List installed packages using DNF.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute dnf list installed."""

        result = subprocess.run(
            [
                "dnf5",
                "list",
                "--installed",
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

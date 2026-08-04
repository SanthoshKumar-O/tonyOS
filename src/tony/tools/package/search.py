"""Package search tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePackageTool


class PackageSearchTool(BasePackageTool):
    """Searches for packages using DNF."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="package_search",
            description="Search for a package using DNF.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute dnf search."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Search term is required.",
            )

        query = arguments[0].value

        result = subprocess.run(
            [
                "dnf5",
                "search",
                query,
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

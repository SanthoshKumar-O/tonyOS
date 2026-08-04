"""Python package install tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePythonTool


class PythonInstallTool(BasePythonTool):
    """Installs a Python package using pip."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="python_install",
            description="Install a Python package using pip.",
            capability=ToolCapability.PYTHON,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Install a Python package."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Package name is required.",
            )

        package = arguments[0].value

        result = subprocess.run(
            [
                "python3",
                "-m",
                "pip",
                "install",
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

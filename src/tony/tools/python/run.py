"""Python run tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePythonTool


class PythonRunTool(BasePythonTool):
    """Executes inline Python code."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="python_run",
            description="Execute inline Python code.",
            capability=ToolCapability.PYTHON,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute inline Python code."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Python code is required.",
            )

        code = arguments[0].value

        result = subprocess.run(
            [
                "python3",
                "-c",
                code,
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

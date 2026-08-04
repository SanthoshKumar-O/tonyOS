"""Python execute tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePythonTool


class PythonExecuteTool(BasePythonTool):
    """Executes a Python script."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="python_execute",
            description="Execute a Python script.",
            capability=ToolCapability.PYTHON,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute a Python script."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Python script path is required.",
            )

        script = arguments[0].value

        result = subprocess.run(
            [
                "python3",
                script,
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

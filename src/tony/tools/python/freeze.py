"""Python freeze tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePythonTool


class PythonFreezeTool(BasePythonTool):
    """Generates requirements.txt contents."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="python_freeze",
            description="Freeze installed Python packages.",
            capability=ToolCapability.PYTHON,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute pip freeze."""

        result = subprocess.run(
            [
                "python3",
                "-m",
                "pip",
                "freeze",
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

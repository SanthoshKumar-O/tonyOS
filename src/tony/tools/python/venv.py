"""Python virtual environment tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BasePythonTool


class PythonVenvTool(BasePythonTool):
    """Creates a Python virtual environment."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="python_venv",
            description="Create a Python virtual environment.",
            capability=ToolCapability.PYTHON,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Create a virtual environment."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Virtual environment name is required.",
            )

        venv_name = arguments[0].value

        result = subprocess.run(
            [
                "python3",
                "-m",
                "venv",
                venv_name,
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

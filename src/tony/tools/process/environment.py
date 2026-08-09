"""Process environment inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessEnvironmentTool(BaseProcessTool):
    """Show environment variables of a running process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_environment",
            description="Show environment variables of a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read environment variables from /proc."""

        if not arguments:
            return ToolResult(
                success=False,
                error="Process ID is required.",
            )

        pid = arguments[0].value.strip()

        if not pid:
            return ToolResult(
                success=False,
                error="Process ID cannot be empty.",
            )

        if not pid.isdigit() or int(pid) <= 0:
            return ToolResult(
                success=False,
                error="Process ID must be a positive integer.",
            )

        environment_path = Path("/proc") / pid / "environ"

        try:
            data = environment_path.read_bytes()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading environment of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not data:
            return ToolResult(
                success=True,
                output="",
                exit_code=0,
            )

        variables = data.rstrip(b"\0").split(b"\0")

        decoded: list[str] = []

        for variable in variables:
            try:
                decoded.append(variable.decode())
            except UnicodeDecodeError:
                decoded.append(variable.decode(errors="replace"))

        decoded.sort()

        return ToolResult(
            success=True,
            output="\n".join(decoded),
            exit_code=0,
        )
"""Process resource limits inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessLimitsTool(BaseProcessTool):
    """Show resource limits of a running process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_limits",
            description="Show resource limits of a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read resource limits from procfs."""

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

        limits_path = Path("/proc") / pid / "limits"

        try:
            output = limits_path.read_text()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading limits of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        return ToolResult(
            success=True,
            output=output.rstrip(),
            exit_code=0,
        )
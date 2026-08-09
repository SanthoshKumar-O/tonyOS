"""Process status inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessStatusFlagsTool(BaseProcessTool):
    """Show the current kernel state of a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_status_flags",
            description="Show the current kernel state of a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read the process state."""

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

        status_path = Path("/proc") / pid / "status"

        try:
            content = status_path.read_text()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading status of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        state: str | None = None

        for line in content.splitlines():
            if line.startswith("State:"):
                state = line.partition(":")[2].strip()
                break

        if state is None:
            return ToolResult(
                success=False,
                error=f"State information is unavailable for process '{pid}'.",
            )

        return ToolResult(
            success=True,
            output=state,
            exit_code=0,
        )
"""Process file descriptor inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessFdsTool(BaseProcessTool):
    """Show file descriptors opened by a running process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_fds",
            description="Show file descriptors opened by a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read process file descriptor information."""

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

        fd_path = Path("/proc") / pid / "fd"

        try:
            entries = sorted(fd_path.iterdir(), key=lambda entry: entry.name)
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading file descriptors of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        lines: list[str] = []

        for entry in entries:
            try:
                target = entry.resolve()
                lines.append(f"{entry.name}: {target}")
            except PermissionError:
                lines.append(f"{entry.name}: permission denied")
            except OSError:
                lines.append(f"{entry.name}: unavailable")

        return ToolResult(
            success=True,
            output="\n".join(lines),
            exit_code=0,
        )
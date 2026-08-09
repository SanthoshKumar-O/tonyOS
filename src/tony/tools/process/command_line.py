"""Process command-line inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessCommandLineTool(BaseProcessTool):
    """Show the command line used to start a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_command_line",
            description="Show the command line used to start a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read a process command line from procfs."""

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

        command_line_path = Path("/proc") / pid / "cmdline"

        try:
            raw_command_line = command_line_path.read_bytes()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading command line of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not raw_command_line:
            return ToolResult(
                success=True,
                output="",
                exit_code=0,
            )

        command_line = raw_command_line.replace(b"\x00", b" ").decode(
            "utf-8",
            errors="replace",
        ).strip()

        return ToolResult(
            success=True,
            output=command_line,
            exit_code=0,
        )
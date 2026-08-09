"""Process CPU time inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessCpuTimesTool(BaseProcessTool):
    """Show CPU time consumed by a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_cpu_times",
            description="Show user and system CPU time consumed by a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read CPU timing information."""

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

        stat_path = Path("/proc") / pid / "stat"

        try:
            content = stat_path.read_text().strip()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading CPU times of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        fields = self._parse_stat(content)

        if fields is None or len(fields) < 13:
            return ToolResult(
                success=False,
                error=f"CPU time information is unavailable for process '{pid}'.",
            )

        try:
            user_ticks = int(fields[11])
            system_ticks = int(fields[12])
        except ValueError:
            return ToolResult(
                success=False,
                error=f"CPU time information is unavailable for process '{pid}'.",
            )

        total_ticks = user_ticks + system_ticks

        output = (
            f"user_ticks: {user_ticks}\n"
            f"system_ticks: {system_ticks}\n"
            f"total_ticks: {total_ticks}"
        )

        return ToolResult(
            success=True,
            output=output,
            exit_code=0,
        )

    @staticmethod
    def _parse_stat(content: str) -> list[str] | None:
        """Parse /proc/<pid>/stat fields after the command name."""

        closing_paren = content.rfind(")")

        if closing_paren == -1:
            return None

        remainder = content[closing_paren + 1 :].strip()

        if not remainder:
            return None

        return remainder.split()
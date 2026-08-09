"""Process statistics inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessStatsTool(BaseProcessTool):
    """Show core statistics for a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_stats",
            description="Show core statistics for a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read core process statistics."""

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
                error=f"Permission denied reading statistics of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        fields = self._parse_stat(content)

        if fields is None or len(fields) < 22:
            return ToolResult(
                success=False,
                error=f"Process statistics are unavailable for process '{pid}'.",
            )

        try:
            process_state = fields[0]
            parent_pid = int(fields[1])
            process_group_id = int(fields[2])
            session_id = int(fields[3])
            thread_count = int(fields[16])
            start_time = int(fields[19])
            virtual_memory = int(fields[20])
            resident_pages = int(fields[21])
        except (ValueError, IndexError):
            return ToolResult(
                success=False,
                error=f"Process statistics are unavailable for process '{pid}'.",
            )

        output = (
            f"pid: {pid}\n"
            f"state: {process_state}\n"
            f"ppid: {parent_pid}\n"
            f"pgid: {process_group_id}\n"
            f"sid: {session_id}\n"
            f"threads: {thread_count}\n"
            f"start_time: {start_time}\n"
            f"virtual_memory: {virtual_memory}\n"
            f"resident_pages: {resident_pages}"
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
"""Process session inspection tool."""

from __future__ import annotations

import os
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessSessionTool(BaseProcessTool):
    """Show the session and process-group information of a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_session",
            description="Show the session and process-group information of a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read process session information."""

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

        process_id = int(pid)

        try:
            session_id = os.getsid(process_id)
            process_group_id = os.getpgid(process_id)
        except ProcessLookupError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading session of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
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
                error=f"Permission denied reading session of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        parent_pid = self._parse_parent_pid(content)

        output = (
            f"pid: {process_id}\n"
            f"ppid: {parent_pid}\n"
            f"pgid: {process_group_id}\n"
            f"sid: {session_id}"
        )

        return ToolResult(
            success=True,
            output=output,
            exit_code=0,
        )

    @staticmethod
    def _parse_parent_pid(content: str) -> int:
        """Extract the parent PID from /proc status."""

        for line in content.splitlines():
            if line.startswith("PPid:"):
                try:
                    return int(line.partition(":")[2].strip())
                except ValueError:
                    break

        return 0
"""Process CPU affinity inspection tool."""

from __future__ import annotations

import os

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessAffinityTool(BaseProcessTool):
    """Show the CPUs a process is allowed to run on."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_affinity",
            description="Show the CPUs a process is allowed to run on.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read process CPU affinity."""

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
            cpus = sorted(os.sched_getaffinity(process_id))
        except ProcessLookupError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading CPU affinity of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        output = ",".join(str(cpu) for cpu in cpus)

        return ToolResult(
            success=True,
            output=output,
            exit_code=0,
        )
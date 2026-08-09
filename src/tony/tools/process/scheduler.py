"""Process scheduler inspection tool."""

from __future__ import annotations

import os

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessSchedulerTool(BaseProcessTool):
    """Show the scheduler policy and priority of a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_scheduler",
            description="Show the scheduler policy and priority of a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read process scheduling information."""

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
            policy = os.sched_getscheduler(process_id)
            priority = os.getpriority(os.PRIO_PROCESS, process_id)
        except ProcessLookupError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading scheduler information for process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        policy_name = self._policy_name(policy)

        output = (
            f"policy: {policy_name}\n"
            f"priority: {priority}"
        )

        return ToolResult(
            success=True,
            output=output,
            exit_code=0,
        )

    @staticmethod
    def _policy_name(policy: int) -> str:
        """Return a readable scheduler policy name."""

        policies = {
            getattr(os, "SCHED_OTHER", 0): "SCHED_OTHER",
            getattr(os, "SCHED_FIFO", 1): "SCHED_FIFO",
            getattr(os, "SCHED_RR", 2): "SCHED_RR",
            getattr(os, "SCHED_BATCH", 3): "SCHED_BATCH",
            getattr(os, "SCHED_IDLE", 5): "SCHED_IDLE",
            getattr(os, "SCHED_DEADLINE", 6): "SCHED_DEADLINE",
        }

        return policies.get(policy, str(policy))
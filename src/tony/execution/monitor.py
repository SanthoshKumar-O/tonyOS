"""Execution monitor."""

from __future__ import annotations

from .models import (
    ExecutionEvent,
    ExecutionStatus,
)
from .protocols import ExecutionMonitorProtocol


class ExecutionMonitor(ExecutionMonitorProtocol):
    """Monitors tool execution."""

    def start(
        self,
        tool: str,
    ) -> ExecutionEvent:
        """Create a started execution event."""

        return ExecutionEvent(
            status=ExecutionStatus.STARTED,
            tool=tool,
        )

    def complete(
        self,
        tool: str,
    ) -> ExecutionEvent:
        """Create a completed execution event."""

        return ExecutionEvent(
            status=ExecutionStatus.COMPLETED,
            tool=tool,
        )

    def fail(
        self,
        tool: str,
    ) -> ExecutionEvent:
        """Create a failed execution event."""

        return ExecutionEvent(
            status=ExecutionStatus.FAILED,
            tool=tool,
        )

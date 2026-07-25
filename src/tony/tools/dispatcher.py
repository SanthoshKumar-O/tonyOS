"""Tool dispatcher."""

from __future__ import annotations

from tony.execution import ExecutionMonitor
from tony.recovery import RecoveryEngine
from tony.tools.models import (
    ToolArgument,
    ToolResult,
    ToolSelection,
)
from tony.tools.protocols import (
    ToolRegistryProtocol,
)


class ToolDispatcher:
    """Dispatches tool execution."""

    def __init__(
        self,
        registry: ToolRegistryProtocol,
    ) -> None:
        self._registry = registry
        self._monitor = ExecutionMonitor()
        self._recovery = RecoveryEngine()

    def dispatch(
        self,
        selection: ToolSelection,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the selected tool."""

        tool = self._registry.get(
            selection.tool_name,
        )

        self._monitor.start(
            tool.metadata.name,
        )

        result = tool.execute(arguments)

        if result.success:
            self._monitor.complete(
                tool.metadata.name,
            )
            return result

        self._monitor.fail(
            tool.metadata.name,
        )

        recovery = self._recovery.recover(
            result.error,
        )

        # Recovery decisions will be acted upon in M3.12.
        _ = recovery

        return result

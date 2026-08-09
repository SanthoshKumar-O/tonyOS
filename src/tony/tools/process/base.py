"""Base process tool."""

from __future__ import annotations

from abc import ABC, abstractmethod

from tony.tools import (
    ToolArgument,
    ToolProtocol,
    ToolResult,
)


class BaseProcessTool(
    ToolProtocol,
    ABC,
):
    """Base class for process-management tools."""

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the process tool safely."""

        try:
            return self._execute(arguments)

        except Exception as error:
            return ToolResult(
                success=False,
                output="",
                error=str(error),
            )

    @abstractmethod
    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the process operation."""
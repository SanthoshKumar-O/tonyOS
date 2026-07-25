"""Base filesystem tool."""

from __future__ import annotations

from abc import ABC, abstractmethod

from tony.tools import (
    ToolArgument,
    ToolProtocol,
    ToolResult,
)


class BaseFilesystemTool(
    ToolProtocol,
    ABC,
):
    """Base class for filesystem tools."""

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the tool safely."""

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
        """Execute the filesystem tool."""

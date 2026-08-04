"""Base terminal tool."""

from __future__ import annotations

import subprocess
from abc import ABC, abstractmethod

from tony.tools import (
    ToolArgument,
    ToolProtocol,
    ToolResult,
)


class BaseTerminalTool(
    ToolProtocol,
    ABC,
):
    """Base class for terminal tools."""

    _TIMEOUT = 120

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the tool safely."""

        try:
            return self._execute(arguments)

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                output="",
                error="Terminal command timed out.",
            )

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
        """Execute the terminal tool."""

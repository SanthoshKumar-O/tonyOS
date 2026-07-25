"""Tool registry."""

from __future__ import annotations

from tony.tools.exceptions import (
    ToolRegistrationError,
)
from tony.tools.protocols import ToolProtocol


class ToolRegistry:
    """Stores registered tools."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolProtocol] = {}

    def register(
        self,
        tool: ToolProtocol,
    ) -> None:
        """Register a tool."""

        name = tool.metadata.name

        if name in self._tools:
            raise ToolRegistrationError(
                f"Tool '{name}' is already registered.",
            )

        self._tools[name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:
        """Remove a registered tool."""

        self._tools.pop(name, None)

    def get(
        self,
        name: str,
    ) -> ToolProtocol:
        """Return a registered tool."""

        try:
            return self._tools[name]
        except KeyError as error:
            raise ToolRegistrationError(
                f"Unknown tool '{name}'.",
            ) from error

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether a tool is registered."""

        return name in self._tools

    def tools(
        self,
    ) -> list[ToolProtocol]:
        """Return all registered tools."""

        return list(self._tools.values())

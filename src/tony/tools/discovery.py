"""Tool discovery service."""

from __future__ import annotations

from tony.tools.exceptions import ToolDiscoveryError
from tony.tools.models import (
    ToolCapability,
    ToolSelection,
)
from tony.tools.protocols import ToolRegistryProtocol


class ToolDiscovery:
    """Discovers an appropriate tool for execution."""

    def __init__(
        self,
        registry: ToolRegistryProtocol,
    ) -> None:
        self._registry = registry

    def discover(
        self,
        capability: ToolCapability,
    ) -> ToolSelection:
        """Select a tool matching the requested capability."""

        for tool in self._registry.tools():
            if tool.metadata.capability is capability:
                return ToolSelection(
                    tool_name=tool.metadata.name,
                    confidence=1.0,
                    reason=(
                        f"Selected tool '{tool.metadata.name}' for capability '{capability.value}'."
                    ),
                )

        raise ToolDiscoveryError(
            f"No tool registered for capability '{capability.value}'.",
        )

"""Permission engine."""

from __future__ import annotations

from tony.tools.exceptions import ToolRegistrationError
from tony.tools.models import (
    PermissionDecision,
    ToolCapability,
    ToolSelection,
)
from tony.tools.protocols import ToolRegistryProtocol


class PermissionEngine:
    """Determines whether a selected tool is allowed to execute."""

    _ALLOWED_CAPABILITIES = {
        ToolCapability.FILESYSTEM,
        ToolCapability.SHELL,
        ToolCapability.GIT,
        ToolCapability.PYTHON,
    }

    def __init__(
        self,
        registry: ToolRegistryProtocol,
    ) -> None:
        self._registry = registry

    def check(
        self,
        selection: ToolSelection,
    ) -> PermissionDecision:
        """Check whether the selected tool is permitted."""

        try:
            tool = self._registry.get(selection.tool_name)

        except ToolRegistrationError:
            return PermissionDecision(
                allowed=False,
                reason=f"Unknown tool '{selection.tool_name}'.",
            )

        capability = tool.metadata.capability

        if capability in self._ALLOWED_CAPABILITIES:
            return PermissionDecision(
                allowed=True,
                reason=(f"Capability '{capability.value}' is permitted."),
            )

        return PermissionDecision(
            allowed=False,
            reason=(f"Capability '{capability.value}' is not permitted."),
        )

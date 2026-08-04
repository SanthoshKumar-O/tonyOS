"""Systemctl tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .disable import SystemctlDisableTool
from .enable import SystemctlEnableTool
from .restart import SystemctlRestartTool
from .start import SystemctlStartTool
from .status import SystemctlStatusTool
from .stop import SystemctlStopTool


class SystemctlRegistry:
    """Registers systemctl tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register systemctl tools."""

        registry.register(
            SystemctlStartTool(),
        )
        registry.register(
            SystemctlStopTool(),
        )
        registry.register(
            SystemctlRestartTool(),
        )
        registry.register(
            SystemctlEnableTool(),
        )
        registry.register(
            SystemctlDisableTool(),
        )
        registry.register(
            SystemctlStatusTool(),
        )

"""Package tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .install import PackageInstallTool
from .list import PackageListTool
from .remove import PackageRemoveTool
from .search import PackageSearchTool
from .update import PackageUpdateTool


class PackageRegistry:
    """Registers package tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register package tools."""

        registry.register(
            PackageInstallTool(),
        )
        registry.register(
            PackageRemoveTool(),
        )
        registry.register(
            PackageUpdateTool(),
        )
        registry.register(
            PackageSearchTool(),
        )
        registry.register(
            PackageListTool(),
        )

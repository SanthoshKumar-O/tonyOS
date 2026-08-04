"""Python tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .execute import PythonExecuteTool
from .freeze import PythonFreezeTool
from .install import PythonInstallTool
from .list import PythonListTool
from .run import PythonRunTool
from .venv import PythonVenvTool


class PythonRegistry:
    """Registers Python tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register Python tools."""

        registry.register(
            PythonExecuteTool(),
        )
        registry.register(
            PythonRunTool(),
        )
        registry.register(
            PythonVenvTool(),
        )
        registry.register(
            PythonInstallTool(),
        )
        registry.register(
            PythonListTool(),
        )
        registry.register(
            PythonFreezeTool(),
        )

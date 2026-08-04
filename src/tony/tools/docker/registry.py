"""Docker tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .build import DockerBuildTool
from .images import DockerImagesTool
from .ps import DockerPsTool
from .pull import DockerPullTool
from .rm import DockerRmTool
from .run import DockerRunTool
from .stop import DockerStopTool


class DockerRegistry:
    """Registers Docker tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register Docker tools."""

        registry.register(
            DockerPsTool(),
        )
        registry.register(
            DockerImagesTool(),
        )
        registry.register(
            DockerPullTool(),
        )
        registry.register(
            DockerRunTool(),
        )
        registry.register(
            DockerStopTool(),
        )
        registry.register(
            DockerRmTool(),
        )
        registry.register(
            DockerBuildTool(),
        )

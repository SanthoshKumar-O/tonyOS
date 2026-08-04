"""Git tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .add import GitAddTool
from .branch import GitBranchTool
from .checkout import GitCheckoutTool
from .clone import GitCloneTool
from .commit import GitCommitTool
from .diff import GitDiffTool
from .init import GitInitTool
from .log import GitLogTool
from .status import GitStatusTool


class GitRegistry:
    """Registers Git tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register Git tools."""

        registry.register(
            GitInitTool(),
        )

        registry.register(
            GitStatusTool(),
        )

        registry.register(
            GitAddTool(),
        )

        registry.register(
            GitCommitTool(),
        )

        registry.register(
            GitBranchTool(),
        )

        registry.register(
            GitCheckoutTool(),
        )

        registry.register(
            GitLogTool(),
        )

        registry.register(
            GitDiffTool(),
        )

        registry.register(
            GitCloneTool(),
        )

"""Workspace tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .project_detect import ProjectDetectTool
from .workspace_info import WorkspaceInfoTool
from .workspace_list import WorkspaceListTool
from .workspace_root import WorkspaceRootTool


def register_workspace_tools(
    registry: ToolRegistry,
) -> None:
    """Register all workspace tools."""

    registry.register(WorkspaceRootTool())
    registry.register(ProjectDetectTool())
    registry.register(WorkspaceInfoTool())
    registry.register(WorkspaceListTool())
"""Workspace information tool."""

from __future__ import annotations

import platform
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseWorkspaceTool
from .project_detect import ProjectDetectTool
from .workspace_root import WorkspaceRootTool


class WorkspaceInfoTool(BaseWorkspaceTool):
    """Return information about the current workspace."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="workspace_info",
            description="Show information about the current workspace.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Collect workspace information."""

        current = Path.cwd().resolve()

        root_result = WorkspaceRootTool().execute([])
        project_result = ProjectDetectTool().execute([])

        if not root_result.success:
            return root_result

        if not project_result.success:
            return project_result

        root = root_result.output
        project_types = project_result.output

        try:
            entries = list(current.iterdir())
            directories = sum(entry.is_dir() for entry in entries)
            files = sum(entry.is_file() for entry in entries)
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        output = (
            f"Path: {current}\n"
            f"Root: {root}\n"
            f"Platform: {platform.system()}\n"
            f"Project types: {project_types}\n"
            f"Directories: {directories}\n"
            f"Files: {files}"
        )

        return ToolResult(
            success=True,
            output=output,
        )
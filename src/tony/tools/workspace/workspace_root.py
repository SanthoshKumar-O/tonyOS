"""Workspace root detection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseWorkspaceTool


class WorkspaceRootTool(BaseWorkspaceTool):
    """Find the root of the current workspace."""

    _MARKERS = (
        ".git",
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "CMakeLists.txt",
    )

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="workspace_root",
            description="Find the root directory of the current workspace.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Find the workspace root."""

        current = Path.cwd().resolve()

        for directory in (
            current,
            *current.parents,
        ):
            if any(
                (directory / marker).exists()
                for marker in self._MARKERS
            ):
                return ToolResult(
                    success=True,
                    output=str(directory),
                )

        return ToolResult(
            success=True,
            output=str(current),
        )
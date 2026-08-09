"""Workspace listing tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseWorkspaceTool


class WorkspaceListTool(BaseWorkspaceTool):
    """List entries in the current workspace."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="workspace_list",
            description="List files and directories in the current workspace.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """List workspace entries."""

        current = Path.cwd().resolve()

        try:
            entries = sorted(
                current.iterdir(),
                key=lambda entry: (not entry.is_dir(), entry.name.lower()),
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not entries:
            return ToolResult(
                success=True,
                output="Workspace is empty.",
            )

        lines: list[str] = []

        for entry in entries:
            if entry.is_dir():
                entry_type = "DIR"
            elif entry.is_file():
                entry_type = "FILE"
            else:
                entry_type = "OTHER"

            lines.append(f"{entry_type}\t{entry.name}")

        return ToolResult(
            success=True,
            output="\n".join(lines),
        )
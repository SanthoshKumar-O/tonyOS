"""Process children inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessChildrenTool(BaseProcessTool):
    """Show the direct child processes of a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_children",
            description="Show the direct child processes of a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read direct child process IDs."""

        if not arguments:
            return ToolResult(
                success=False,
                error="Process ID is required.",
            )

        pid = arguments[0].value.strip()

        if not pid:
            return ToolResult(
                success=False,
                error="Process ID cannot be empty.",
            )

        if not pid.isdigit() or int(pid) <= 0:
            return ToolResult(
                success=False,
                error="Process ID must be a positive integer.",
            )

        children_path = (
            Path("/proc")
            / pid
            / "task"
            / pid
            / "children"
        )

        try:
            content = children_path.read_text().strip()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading children of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        if not content:
            return ToolResult(
                success=True,
                output="",
                exit_code=0,
            )

        children = content.split()

        return ToolResult(
            success=True,
            output=" ".join(children),
            exit_code=0,
        )
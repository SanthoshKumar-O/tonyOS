"""Process file descriptor inspection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessFileDescriptorsTool(BaseProcessTool):
    """Show file descriptors opened by a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_file_descriptors",
            description="Show file descriptors opened by a running process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Inspect a process file descriptor directory."""

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

        fd_path = Path("/proc") / pid / "fd"

        try:
            descriptors = sorted(
                fd_path.iterdir(),
                key=lambda path: int(path.name),
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading file descriptors of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        output: list[str] = []

        for descriptor in descriptors:
            try:
                target = descriptor.resolve()
            except OSError:
                target = Path("<unavailable>")

            output.append(f"{descriptor.name} -> {target}")

        return ToolResult(
            success=True,
            output="\n".join(output),
            exit_code=0,
        )
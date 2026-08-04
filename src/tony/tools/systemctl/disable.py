"""Systemctl disable tool."""

from __future__ import annotations

import subprocess

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseSystemctlTool


class SystemctlDisableTool(BaseSystemctlTool):
    """Disables a systemd service."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="systemctl_disable",
            description="Disable a systemd service.",
            capability=ToolCapability.SHELL,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute systemctl disable."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="Service name is required.",
            )

        service = arguments[0].value

        result = subprocess.run(
            [
                "sudo",
                "systemctl",
                "disable",
                service,
            ],
            capture_output=True,
            text=True,
            timeout=self._TIMEOUT,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )

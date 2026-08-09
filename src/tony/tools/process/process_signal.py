"""Process signal tool."""

from __future__ import annotations

import os
import signal

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessSignalTool(BaseProcessTool):
    """Send a signal to a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_signal",
            description="Send a signal to a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Send the requested signal."""

        if len(arguments) < 2:
            return ToolResult(
                success=False,
                error="Process ID and signal are required.",
            )

        pid = arguments[0].value.strip()
        signal_value = arguments[1].value.strip().upper()

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

        if signal_value.startswith("SIG"):
            signal_name = signal_value
        else:
            signal_name = f"SIG{signal_value}"

        if not hasattr(signal, signal_name):
            return ToolResult(
                success=False,
                error=f"Unknown signal '{arguments[1].value}'.",
            )

        process_id = int(pid)
        signal_number = getattr(signal, signal_name)

        try:
            os.kill(process_id, signal_number)
        except ProcessLookupError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied sending {signal_name} to process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        return ToolResult(
            success=True,
            output=f"Sent {signal_name} to process '{pid}'.",
            exit_code=0,
        )
"""Process identity inspection tool."""

from __future__ import annotations

import pwd
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseProcessTool


class ProcessIdentityTool(BaseProcessTool):
    """Show the user and group identity of a process."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="process_identity",
            description="Show the user and group identity of a process.",
            capability=ToolCapability.SYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Read process UID and GID information."""

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

        status_path = Path("/proc") / pid / "status"

        try:
            content = status_path.read_text()
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error=f"Process '{pid}' was not found.",
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error=f"Permission denied reading identity of process '{pid}'.",
            )
        except OSError as error:
            return ToolResult(
                success=False,
                error=str(error),
            )

        uid_values = self._parse_ids(content, "Uid:")
        gid_values = self._parse_ids(content, "Gid:")

        if uid_values is None or gid_values is None:
            return ToolResult(
                success=False,
                error=f"Identity information is unavailable for process '{pid}'.",
            )

        real_uid, effective_uid = uid_values[:2]
        real_gid, effective_gid = gid_values[:2]

        username = self._username(real_uid)

        output = (
            f"uid: {real_uid}\n"
            f"euid: {effective_uid}\n"
            f"user: {username}\n"
            f"gid: {real_gid}\n"
            f"egid: {effective_gid}"
        )

        return ToolResult(
            success=True,
            output=output,
            exit_code=0,
        )

    @staticmethod
    def _parse_ids(
        content: str,
        prefix: str,
    ) -> list[int] | None:
        """Parse numeric IDs from /proc status."""

        for line in content.splitlines():
            if line.startswith(prefix):
                values = line.partition(":")[2].split()

                try:
                    return [int(value) for value in values]
                except ValueError:
                    return None

        return None

    @staticmethod
    def _username(uid: int) -> str:
        """Return the username for a UID."""

        try:
            return pwd.getpwuid(uid).pw_name
        except KeyError:
            return str(uid)
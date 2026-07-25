"""Execution service."""

from __future__ import annotations

from tony.tools import (
    ArgumentValidator,
    PermissionEngine,
    ToolArgument,
    ToolDispatcher,
    ToolResult,
    ToolSelection,
)


class ExecutionService:
    """Coordinates tool execution."""

    def __init__(
        self,
        permission_engine: PermissionEngine,
        argument_validator: ArgumentValidator,
        dispatcher: ToolDispatcher,
    ) -> None:
        self._permission_engine = permission_engine
        self._argument_validator = argument_validator
        self._dispatcher = dispatcher

    def execute(
        self,
        selection: ToolSelection,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute a tool."""

        permission = self._permission_engine.check(
            selection,
        )

        if not permission.allowed:
            return ToolResult(
                success=False,
                output="",
                error=permission.reason,
            )

        validation = self._argument_validator.validate(
            selection,
            arguments,
        )

        if not validation.valid:
            return ToolResult(
                success=False,
                output="",
                error=validation.reason,
            )

        return self._dispatcher.dispatch(
            selection,
            arguments,
        )

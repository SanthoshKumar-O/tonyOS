"""Tests for the execution service."""

from __future__ import annotations

from tony.execution.service import ExecutionService
from tony.tools import (
    ArgumentValidator,
    PermissionEngine,
    ToolDispatcher,
    ToolRegistry,
    ToolSelection,
)
from tony.tools.filesystem import PwdTool


def create_service() -> ExecutionService:
    """Create an execution service for testing."""

    registry = ToolRegistry()
    registry.register(PwdTool())

    dispatcher = ToolDispatcher(registry)

    return ExecutionService(
        permission_engine=PermissionEngine(
            registry,
        ),
        argument_validator=ArgumentValidator(),
        dispatcher=dispatcher,
    )


def test_execute_success() -> None:
    service = create_service()

    selection = ToolSelection(
        tool_name="pwd",
        confidence=1.0,
        reason="Test selection",
    )

    result = service.execute(
        selection,
        [],
    )

    assert result.success is True
    assert result.error == ""
    assert result.output != ""


def test_execute_unknown_tool() -> None:
    service = create_service()

    selection = ToolSelection(
        tool_name="unknown",
        confidence=1.0,
        reason="Test selection",
    )

    result = service.execute(
        selection,
        [],
    )

    assert result.success is False

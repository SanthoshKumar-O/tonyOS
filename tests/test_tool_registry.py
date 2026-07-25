from __future__ import annotations

import pytest

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolProtocol,
    ToolRegistrationError,
    ToolRegistry,
    ToolResult,
)


class DummyTool(ToolProtocol):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="dummy",
            description="Dummy tool",
            capability=ToolCapability.SYSTEM,
        )

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        return ToolResult(
            success=True,
            output="Executed",
        )


def test_register_tool() -> None:
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    assert registry.exists("dummy")
    assert registry.get("dummy") is tool


def test_register_duplicate_tool() -> None:
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    with pytest.raises(ToolRegistrationError):
        registry.register(tool)


def test_unregister_tool() -> None:
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)
    registry.unregister("dummy")

    assert not registry.exists("dummy")


def test_get_unknown_tool() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolRegistrationError):
        registry.get("unknown")


def test_tools() -> None:
    registry = ToolRegistry()

    tool = DummyTool()

    registry.register(tool)

    tools = registry.tools()

    assert len(tools) == 1
    assert tools[0] is tool

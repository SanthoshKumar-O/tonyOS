from __future__ import annotations

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolDispatcher,
    ToolMetadata,
    ToolProtocol,
    ToolRegistry,
    ToolResult,
    ToolSelection,
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
            output=f"Executed with {len(arguments)} arguments.",
        )


def test_dispatch_tool() -> None:
    registry = ToolRegistry()
    registry.register(DummyTool())

    dispatcher = ToolDispatcher(registry)

    result = dispatcher.dispatch(
        ToolSelection(
            tool_name="dummy",
            confidence=1.0,
            reason="Dummy selection.",
        ),
        [
            ToolArgument(
                name="path",
                value="/tmp",
            ),
        ],
    )

    assert result.success is True
    assert result.output == "Executed with 1 arguments."

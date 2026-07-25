from __future__ import annotations

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolProtocol,
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


def test_tool_protocol() -> None:
    tool = DummyTool()

    assert tool.metadata.name == "dummy"
    assert tool.metadata.capability is ToolCapability.SYSTEM

    result = tool.execute([])

    assert result.success is True
    assert result.output == "Executed"

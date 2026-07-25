from __future__ import annotations

from tony.tools import (
    PermissionEngine,
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolProtocol,
    ToolRegistry,
    ToolResult,
    ToolSelection,
)


class DummyFilesystemTool(ToolProtocol):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="mkdir",
            description="Create directories",
            capability=ToolCapability.FILESYSTEM,
        )

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        return ToolResult(
            success=True,
        )


class DummyNetworkTool(ToolProtocol):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="download",
            description="Download files",
            capability=ToolCapability.NETWORK,
        )

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        return ToolResult(
            success=True,
        )


def test_allow_filesystem_tool() -> None:
    registry = ToolRegistry()
    registry.register(DummyFilesystemTool())

    engine = PermissionEngine(registry)

    decision = engine.check(
        ToolSelection(
            tool_name="mkdir",
            confidence=1.0,
            reason="Filesystem operation.",
        ),
    )

    assert decision.allowed is True
    assert "permitted" in decision.reason.lower()


def test_deny_network_tool() -> None:
    registry = ToolRegistry()
    registry.register(DummyNetworkTool())

    engine = PermissionEngine(registry)

    decision = engine.check(
        ToolSelection(
            tool_name="download",
            confidence=1.0,
            reason="Network operation.",
        ),
    )

    assert decision.allowed is False
    assert "not permitted" in decision.reason.lower()

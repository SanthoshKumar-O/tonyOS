from __future__ import annotations

import pytest

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolDiscovery,
    ToolDiscoveryError,
    ToolMetadata,
    ToolProtocol,
    ToolRegistry,
    ToolResult,
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
            output="Directory created.",
        )


class DummyShellTool(ToolProtocol):
    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="shell",
            description="Execute shell commands",
            capability=ToolCapability.SHELL,
        )

    def execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        return ToolResult(
            success=True,
            output="Command executed.",
        )


def test_discover_filesystem_tool() -> None:
    registry = ToolRegistry()
    registry.register(DummyFilesystemTool())
    registry.register(DummyShellTool())

    discovery = ToolDiscovery(registry)

    selection = discovery.discover(
        ToolCapability.FILESYSTEM,
    )

    assert selection.tool_name == "mkdir"
    assert selection.confidence == 1.0
    assert "filesystem" in selection.reason.lower()


def test_discover_shell_tool() -> None:
    registry = ToolRegistry()
    registry.register(DummyFilesystemTool())
    registry.register(DummyShellTool())

    discovery = ToolDiscovery(registry)

    selection = discovery.discover(
        ToolCapability.SHELL,
    )

    assert selection.tool_name == "shell"
    assert selection.confidence == 1.0


def test_discover_unknown_capability() -> None:
    registry = ToolRegistry()

    discovery = ToolDiscovery(registry)

    with pytest.raises(ToolDiscoveryError):
        discovery.discover(
            ToolCapability.SYSTEM,
        )

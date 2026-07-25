from tony.tools import ToolRegistry

from . import (
    CatTool,
    CpTool,
    LsTool,
    MkdirTool,
    MvTool,
    PwdTool,
    RmTool,
    TouchTool,
)


def register_filesystem_tools(
    registry: ToolRegistry,
) -> None:
    """Register all filesystem tools."""

    registry.register(PwdTool())
    registry.register(LsTool())
    registry.register(MkdirTool())
    registry.register(TouchTool())
    registry.register(CatTool())
    registry.register(CpTool())
    registry.register(MvTool())
    registry.register(RmTool())

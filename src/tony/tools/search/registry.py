"""Search tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .search_directory import SearchDirectoryTool
from .search_files import SearchFilesTool
from .search_text import SearchTextTool


def register_search_tools(
    registry: ToolRegistry,
) -> None:
    """Register all search tools."""

    registry.register(SearchFilesTool())
    registry.register(SearchTextTool())
    registry.register(SearchDirectoryTool())
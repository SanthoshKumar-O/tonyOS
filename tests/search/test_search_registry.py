"""Tests for the Search tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.search import register_search_tools


def test_registers_all_search_tools() -> None:
    registry = ToolRegistry()

    register_search_tools(registry)

    assert registry.exists("search_files")
    assert registry.exists("search_text")
    assert registry.exists("search_directory")


def test_registers_exactly_three_search_tools() -> None:
    registry = ToolRegistry()

    register_search_tools(registry)

    assert len(registry.tools()) == 3
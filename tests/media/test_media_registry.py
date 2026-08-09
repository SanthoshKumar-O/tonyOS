"""Tests for the media tool registry."""

from tony.tools import ToolRegistry
from tony.tools.media import register_media_tools


def test_registers_media_tools() -> None:
    registry = ToolRegistry()

    register_media_tools(registry)

    assert registry.get("open_image").metadata.name == "open_image"
    assert registry.get("open_pdf").metadata.name == "open_pdf"
    assert registry.get("play_audio").metadata.name == "play_audio"
    assert registry.get("thumbnail").metadata.name == "thumbnail"
"""Media tool registry."""

from tony.tools import ToolRegistry

from .open_image import OpenImageTool
from .open_pdf import OpenPdfTool
from .play_audio import PlayAudioTool
from .thumbnail import ThumbnailTool


def register_media_tools(
    registry: ToolRegistry,
) -> None:
    """Register all media tools."""

    registry.register(OpenImageTool())
    registry.register(OpenPdfTool())
    registry.register(PlayAudioTool())
    registry.register(ThumbnailTool())
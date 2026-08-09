"""Archive tool registry."""

from tony.tools import ToolRegistry

from .tar import TarTool
from .untar import UntarTool
from .unzip import UnzipTool
from .zip import ZipTool


def register_archive_tools(
    registry: ToolRegistry,
) -> None:
    """Register all archive tools."""

    registry.register(ZipTool())
    registry.register(UnzipTool())
    registry.register(TarTool())
    registry.register(UntarTool())

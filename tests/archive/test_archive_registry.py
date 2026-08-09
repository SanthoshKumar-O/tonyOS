from tony.tools import ToolRegistry
from tony.tools.archive import register_archive_tools


def test_register_archive_tools() -> None:
    registry = ToolRegistry()

    register_archive_tools(registry)

    assert registry.exists("zip")
    assert registry.exists("unzip")
    assert registry.exists("tar")
    assert registry.exists("untar")

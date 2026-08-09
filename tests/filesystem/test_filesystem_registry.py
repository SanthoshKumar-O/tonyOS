from tony.tools import ToolRegistry
from tony.tools.filesystem.registry import register_filesystem_tools


def test_register_filesystem_tools() -> None:
    registry = ToolRegistry()

    register_filesystem_tools(registry)

    assert registry.exists("pwd")
    assert registry.exists("ls")
    assert registry.exists("mkdir")
    assert registry.exists("touch")
    assert registry.exists("cat")
    assert registry.exists("cp")
    assert registry.exists("mv")
    assert registry.exists("rm")

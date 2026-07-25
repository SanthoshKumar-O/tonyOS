from __future__ import annotations

from pathlib import Path

from tony.tools.filesystem import PwdTool


def test_pwd_tool() -> None:
    tool = PwdTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == str(Path.cwd())
    assert result.error == ""


def test_pwd_tool_metadata() -> None:
    tool = PwdTool()

    metadata = tool.metadata

    assert metadata.name == "pwd"
    assert metadata.description == "Print the current working directory."

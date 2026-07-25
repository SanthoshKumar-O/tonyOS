from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import LsTool


def test_ls_current_directory() -> None:
    tool = LsTool()

    result = tool.execute([])

    assert result.success is True
    assert result.error == ""


def test_ls_specific_directory(tmp_path: Path) -> None:
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()

    tool = LsTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(tmp_path),
            ),
        ],
    )

    assert result.success is True

    entries = result.output.splitlines()

    assert "a.txt" in entries
    assert "b.txt" in entries


def test_ls_missing_directory() -> None:
    tool = LsTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value="/this/path/does/not/exist",
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_ls_metadata() -> None:
    tool = LsTool()

    metadata = tool.metadata

    assert metadata.name == "ls"
    assert metadata.description == "List directory contents."

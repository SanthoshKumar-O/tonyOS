from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import RmTool


def test_rm_removes_file(
    tmp_path: Path,
) -> None:
    tool = RmTool()

    file_path = tmp_path / "example.txt"

    file_path.write_text(
        "Tony",
        encoding="utf-8",
    )

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(file_path),
            ),
        ],
    )

    assert result.success is True
    assert not file_path.exists()
    assert result.output == str(file_path)
    assert result.error == ""


def test_rm_missing_file() -> None:
    tool = RmTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value="/does/not/exist.txt",
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_rm_without_arguments() -> None:
    tool = RmTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A file path is required."


def test_rm_metadata() -> None:
    tool = RmTool()

    metadata = tool.metadata

    assert metadata.name == "rm"
    assert metadata.description == "Remove a file."

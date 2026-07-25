from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import CatTool


def test_cat_reads_file(
    tmp_path: Path,
) -> None:
    tool = CatTool()

    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "Hello Tony!",
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
    assert result.output == "Hello Tony!"
    assert result.error == ""


def test_cat_missing_file() -> None:
    tool = CatTool()

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


def test_cat_without_arguments() -> None:
    tool = CatTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A file path is required."


def test_cat_metadata() -> None:
    tool = CatTool()

    metadata = tool.metadata

    assert metadata.name == "cat"
    assert metadata.description == "Read the contents of a text file."

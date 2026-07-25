from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import TouchTool


def test_touch_creates_file(
    tmp_path: Path,
) -> None:
    tool = TouchTool()

    file_path = tmp_path / "example.txt"

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(file_path),
            ),
        ],
    )

    assert result.success is True
    assert file_path.exists()
    assert file_path.is_file()
    assert result.output == str(file_path)
    assert result.error == ""


def test_touch_existing_file(
    tmp_path: Path,
) -> None:
    tool = TouchTool()

    file_path = tmp_path / "existing.txt"
    file_path.touch()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(file_path),
            ),
        ],
    )

    assert result.success is True
    assert file_path.exists()


def test_touch_without_arguments() -> None:
    tool = TouchTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A file path is required."


def test_touch_metadata() -> None:
    tool = TouchTool()

    metadata = tool.metadata

    assert metadata.name == "touch"
    assert metadata.description == "Create an empty file."

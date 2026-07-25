from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
)
from tony.tools.filesystem import MkdirTool


def test_mkdir_creates_directory(
    tmp_path: Path,
) -> None:
    tool = MkdirTool()

    directory = tmp_path / "example"

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(directory),
            ),
        ],
    )

    assert result.success is True
    assert directory.exists()
    assert directory.is_dir()
    assert result.output == str(directory)
    assert result.error == ""


def test_mkdir_existing_directory(
    tmp_path: Path,
) -> None:
    tool = MkdirTool()

    directory = tmp_path / "existing"
    directory.mkdir()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(directory),
            ),
        ],
    )

    assert result.success is True
    assert directory.exists()


def test_mkdir_without_arguments() -> None:
    tool = MkdirTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A directory path is required."


def test_mkdir_metadata() -> None:
    tool = MkdirTool()

    metadata = tool.metadata

    assert metadata.name == "mkdir"
    assert metadata.description == "Create a directory."

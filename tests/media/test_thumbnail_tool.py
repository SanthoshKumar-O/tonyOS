"""Tests for ThumbnailTool."""

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.media import ThumbnailTool


def test_creates_thumbnail(tmp_path: Path) -> None:
    source = tmp_path / "source.ppm"
    destination = tmp_path / "thumbnail.png"

    source.write_text(
        """P3
2 2
255
255 0 0
0 255 0
0 0 255
255 255 255
""",
        encoding="utf-8",
    )

    tool = ThumbnailTool()

    result = tool.execute(
        [
            ToolArgument(name="source", value=str(source)),
            ToolArgument(name="destination", value=str(destination)),
        ]
    )

    assert result.success
    assert destination.exists()
    assert result.output == str(destination)


def test_requires_source_and_destination(tmp_path: Path) -> None:
    tool = ThumbnailTool()

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(tmp_path / "source.png"),
            )
        ]
    )

    assert not result.success
    assert result.error == "Source and destination paths are required."


def test_source_must_exist(tmp_path: Path) -> None:
    source = tmp_path / "missing.png"
    destination = tmp_path / "thumbnail.png"

    tool = ThumbnailTool()

    result = tool.execute(
        [
            ToolArgument(name="source", value=str(source)),
            ToolArgument(name="destination", value=str(destination)),
        ]
    )

    assert not result.success
    assert result.error == "Source file does not exist."


def test_source_must_be_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "thumbnail.png"

    source.mkdir()

    tool = ThumbnailTool()

    result = tool.execute(
        [
            ToolArgument(name="source", value=str(source)),
            ToolArgument(name="destination", value=str(destination)),
        ]
    )

    assert not result.success
    assert result.error == "Source path must be a file."
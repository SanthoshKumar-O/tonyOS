from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from tony.tools import ToolArgument
from tony.tools.archive import ZipTool


def test_zip_copies_file(
    tmp_path: Path,
) -> None:
    tool = ZipTool()

    source = tmp_path / "source.txt"
    destination = tmp_path / "archive.zip"

    source.write_text(
        "Tony OS",
        encoding="utf-8",
    )

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(source),
            ),
            ToolArgument(
                name="destination",
                value=str(destination),
            ),
        ],
    )

    assert result.success is True
    assert destination.exists()
    assert result.output == str(destination)
    assert result.error == ""

    with ZipFile(destination) as archive:
        assert archive.namelist() == ["source.txt"]
        assert archive.read("source.txt") == b"Tony OS"


def test_zip_directory(
    tmp_path: Path,
) -> None:
    tool = ZipTool()

    source = tmp_path / "project"
    destination = tmp_path / "project.zip"

    source.mkdir()
    (source / "main.py").write_text(
        "print('Tony')",
        encoding="utf-8",
    )
    (source / "README.md").write_text(
        "Tony OS",
        encoding="utf-8",
    )

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(source),
            ),
            ToolArgument(
                name="destination",
                value=str(destination),
            ),
        ],
    )

    assert result.success is True
    assert destination.exists()

    with ZipFile(destination) as archive:
        assert sorted(archive.namelist()) == [
            "project/README.md",
            "project/main.py",
        ]


def test_zip_missing_source(
    tmp_path: Path,
) -> None:
    tool = ZipTool()

    destination = tmp_path / "archive.zip"

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(tmp_path / "missing.txt"),
            ),
            ToolArgument(
                name="destination",
                value=str(destination),
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_zip_without_arguments() -> None:
    tool = ZipTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_zip_metadata() -> None:
    tool = ZipTool()

    metadata = tool.metadata

    assert metadata.name == "zip"
    assert metadata.description == "Create a ZIP archive."

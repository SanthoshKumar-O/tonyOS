from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from tony.tools import ToolArgument
from tony.tools.archive import UnzipTool


def test_unzip_archive(
    tmp_path: Path,
) -> None:
    tool = UnzipTool()

    source = tmp_path / "archive.zip"
    destination = tmp_path / "extracted"

    with ZipFile(source, "w") as archive:
        archive.writestr(
            "hello.txt",
            "Tony OS",
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
    assert (destination / "hello.txt").read_text(
        encoding="utf-8",
    ) == "Tony OS"
    assert result.output == str(destination)
    assert result.error == ""


def test_unzip_invalid_archive(
    tmp_path: Path,
) -> None:
    tool = UnzipTool()

    source = tmp_path / "invalid.zip"
    destination = tmp_path / "extracted"

    source.write_text(
        "not a ZIP archive",
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

    assert result.success is False
    assert result.error != ""


def test_unzip_missing_source(
    tmp_path: Path,
) -> None:
    tool = UnzipTool()

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(tmp_path / "missing.zip"),
            ),
            ToolArgument(
                name="destination",
                value=str(tmp_path / "extracted"),
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_unzip_without_arguments() -> None:
    tool = UnzipTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_unzip_metadata() -> None:
    tool = UnzipTool()

    metadata = tool.metadata

    assert metadata.name == "unzip"
    assert metadata.description == "Extract a ZIP archive."


def test_unzip_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    tool = UnzipTool()

    source = tmp_path / "malicious.zip"
    destination = tmp_path / "extracted"

    with ZipFile(source, "w") as archive:
        archive.writestr(
            "../../outside.txt",
            "unsafe",
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

    assert result.success is False
    assert result.error == "Archive contains an unsafe path."
    assert not (tmp_path / "outside.txt").exists()

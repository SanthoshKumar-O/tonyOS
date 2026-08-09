from __future__ import annotations

import tarfile
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.archive import TarTool


def test_tar_copies_file(
    tmp_path: Path,
) -> None:
    tool = TarTool()

    source = tmp_path / "source.txt"
    destination = tmp_path / "archive.tar"

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

    with tarfile.open(destination) as archive:
        members = archive.getnames()

        assert members == ["source.txt"]

        extracted = archive.extractfile("source.txt")

        assert extracted is not None
        assert extracted.read() == b"Tony OS"


def test_tar_directory(
    tmp_path: Path,
) -> None:
    tool = TarTool()

    source = tmp_path / "project"
    destination = tmp_path / "project.tar"

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

    with tarfile.open(destination) as archive:
        members = sorted(archive.getnames())

        assert members == [
            "project",
            "project/README.md",
            "project/main.py",
        ]


def test_tar_missing_source(
    tmp_path: Path,
) -> None:
    tool = TarTool()

    destination = tmp_path / "archive.tar"

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


def test_tar_without_arguments() -> None:
    tool = TarTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_tar_metadata() -> None:
    tool = TarTool()

    metadata = tool.metadata

    assert metadata.name == "tar"
    assert metadata.description == "Create a TAR archive."

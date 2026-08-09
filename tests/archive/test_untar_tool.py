from __future__ import annotations

import tarfile
from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.archive import UntarTool


def test_untar_archive(
    tmp_path: Path,
) -> None:
    tool = UntarTool()

    source = tmp_path / "archive.tar"
    destination = tmp_path / "extracted"

    file_path = tmp_path / "hello.txt"

    file_path.write_text(
        "Tony OS",
        encoding="utf-8",
    )

    with tarfile.open(source, "w") as archive:
        archive.add(
            file_path,
            arcname="hello.txt",
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


def test_untar_directory_archive(
    tmp_path: Path,
) -> None:
    tool = UntarTool()

    source = tmp_path / "project.tar"
    destination = tmp_path / "extracted"

    project = tmp_path / "project"
    project.mkdir()

    (project / "main.py").write_text(
        "print('Tony')",
        encoding="utf-8",
    )

    (project / "README.md").write_text(
        "Tony OS",
        encoding="utf-8",
    )

    with tarfile.open(source, "w") as archive:
        archive.add(
            project,
            arcname="project",
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

    assert (destination / "project" / "main.py").read_text(
        encoding="utf-8",
    ) == "print('Tony')"

    assert (destination / "project" / "README.md").read_text(
        encoding="utf-8",
    ) == "Tony OS"


def test_untar_invalid_archive(
    tmp_path: Path,
) -> None:
    tool = UntarTool()

    source = tmp_path / "invalid.tar"
    destination = tmp_path / "extracted"

    source.write_text(
        "not a TAR archive",
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


def test_untar_missing_source(
    tmp_path: Path,
) -> None:
    tool = UntarTool()

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value=str(tmp_path / "missing.tar"),
            ),
            ToolArgument(
                name="destination",
                value=str(tmp_path / "extracted"),
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_untar_without_arguments() -> None:
    tool = UntarTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_untar_metadata() -> None:
    tool = UntarTool()

    metadata = tool.metadata

    assert metadata.name == "untar"
    assert metadata.description == "Extract a TAR archive."


def test_untar_rejects_path_traversal(
    tmp_path: Path,
) -> None:
    tool = UntarTool()

    source = tmp_path / "malicious.tar"
    destination = tmp_path / "extracted"

    unsafe_file = tmp_path / "unsafe.txt"

    unsafe_file.write_text(
        "unsafe",
        encoding="utf-8",
    )

    with tarfile.open(source, "w") as archive:
        archive.add(
            unsafe_file,
            arcname="../../outside.txt",
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

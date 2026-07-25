from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import CpTool


def test_cp_copies_file(
    tmp_path: Path,
) -> None:
    tool = CpTool()

    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

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
    assert destination.read_text(encoding="utf-8") == "Tony OS"
    assert result.output == str(destination)
    assert result.error == ""


def test_cp_missing_source() -> None:
    tool = CpTool()

    result = tool.execute(
        [
            ToolArgument(
                name="source",
                value="/does/not/exist.txt",
            ),
            ToolArgument(
                name="destination",
                value="/tmp/output.txt",
            ),
        ],
    )

    assert result.success is False
    assert result.error != ""


def test_cp_without_arguments() -> None:
    tool = CpTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_cp_metadata() -> None:
    tool = CpTool()

    metadata = tool.metadata

    assert metadata.name == "cp"
    assert metadata.description == "Copy a file."

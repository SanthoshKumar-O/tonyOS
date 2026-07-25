from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.filesystem import MvTool


def test_mv_moves_file(
    tmp_path: Path,
) -> None:
    tool = MvTool()

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
    assert not source.exists()
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Tony OS"
    assert result.output == str(destination)
    assert result.error == ""


def test_mv_missing_source() -> None:
    tool = MvTool()

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


def test_mv_without_arguments() -> None:
    tool = MvTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Source and destination paths are required."


def test_mv_metadata() -> None:
    tool = MvTool()

    metadata = tool.metadata

    assert metadata.name == "mv"
    assert metadata.description == "Move a file."

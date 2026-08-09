"""Tests for SearchFilesTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.search import SearchFilesTool


def test_metadata() -> None:
    tool = SearchFilesTool()

    assert tool.metadata.name == "search_files"


def test_finds_matching_files(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "main.py").touch()
    (tmp_path / "test.py").touch()
    (tmp_path / "README.md").touch()

    nested = tmp_path / "src"
    nested.mkdir()
    (nested / "app.py").touch()

    monkeypatch.chdir(tmp_path)

    tool = SearchFilesTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="*.py")]
    )

    assert result.success is True
    assert "main.py" in result.output
    assert "test.py" in result.output
    assert "src/app.py" in result.output
    assert "README.md" not in result.output


def test_no_matches(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").touch()

    monkeypatch.chdir(tmp_path)

    tool = SearchFilesTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="*.py")]
    )

    assert result.success is True
    assert result.output == "No matching files found."


def test_missing_pattern() -> None:
    tool = SearchFilesTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Search pattern is required."


def test_empty_pattern() -> None:
    tool = SearchFilesTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="")]
    )

    assert result.success is False
    assert result.error == "Search pattern cannot be empty."
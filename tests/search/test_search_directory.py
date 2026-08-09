"""Tests for SearchDirectoryTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.search import SearchDirectoryTool


def test_metadata() -> None:
    tool = SearchDirectoryTool()

    assert tool.metadata.name == "search_directory"


def test_finds_matching_directories(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "docs").mkdir()

    nested = tmp_path / "src" / "tools"
    nested.mkdir()

    monkeypatch.chdir(tmp_path)

    tool = SearchDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="*")]
    )

    assert result.success is True
    assert "src" in result.output
    assert "tests" in result.output
    assert "docs" in result.output
    assert "src/tools" in result.output


def test_matches_directory_pattern(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "scripts").mkdir()

    monkeypatch.chdir(tmp_path)

    tool = SearchDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="*src*")]
    )

    assert result.success is True
    assert result.output == "src"


def test_ignores_git_directory(
    monkeypatch,
    tmp_path: Path,
) -> None:
    git_directory = tmp_path / ".git"
    git_directory.mkdir()

    (tmp_path / "src").mkdir()

    monkeypatch.chdir(tmp_path)

    tool = SearchDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="*")]
    )

    assert result.success is True
    assert ".git" not in result.output
    assert "src" in result.output


def test_no_matches(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()

    monkeypatch.chdir(tmp_path)

    tool = SearchDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="missing*")]
    )

    assert result.success is True
    assert result.output == "No matching directories found."


def test_missing_pattern() -> None:
    tool = SearchDirectoryTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Search pattern is required."


def test_empty_pattern() -> None:
    tool = SearchDirectoryTool()

    result = tool.execute(
        [ToolArgument(name="pattern", value="")]
    )

    assert result.success is False
    assert result.error == "Search pattern cannot be empty."
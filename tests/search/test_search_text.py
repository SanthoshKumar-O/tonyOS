"""Tests for SearchTextTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import ToolArgument
from tony.tools.search import SearchTextTool


def test_metadata() -> None:
    tool = SearchTextTool()

    assert tool.metadata.name == "search_text"


def test_finds_matching_text(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "main.py").write_text(
        "print('hello')\nprint('world')\n",
        encoding="utf-8",
    )

    (tmp_path / "config.txt").write_text(
        "hello configuration\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tool = SearchTextTool()

    result = tool.execute(
        [ToolArgument(name="text", value="hello")]
    )

    assert result.success is True
    assert "main.py:1:print('hello')" in result.output
    assert "config.txt:1:hello configuration" in result.output


def test_reports_line_numbers(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "app.py").write_text(
        "first\nsecond\nTARGET\nfourth\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tool = SearchTextTool()

    result = tool.execute(
        [ToolArgument(name="text", value="TARGET")]
    )

    assert result.success is True
    assert result.output == "app.py:3:TARGET"


def test_ignores_git_directory(
    monkeypatch,
    tmp_path: Path,
) -> None:
    git_directory = tmp_path / ".git"
    git_directory.mkdir()

    (git_directory / "config").write_text(
        "secret-target\n",
        encoding="utf-8",
    )

    (tmp_path / "README.md").write_text(
        "normal-target\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tool = SearchTextTool()

    result = tool.execute(
        [ToolArgument(name="text", value="target")]
    )

    assert result.success is True
    assert ".git" not in result.output
    assert "README.md:1:normal-target" in result.output


def test_no_matches(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "README.md").write_text(
        "nothing relevant\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    tool = SearchTextTool()

    result = tool.execute(
        [ToolArgument(name="text", value="missing")]
    )

    assert result.success is True
    assert result.output == "No matching text found."


def test_missing_search_text() -> None:
    tool = SearchTextTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Search text is required."


def test_empty_search_text() -> None:
    tool = SearchTextTool()

    result = tool.execute(
        [ToolArgument(name="text", value="")]
    )

    assert result.success is False
    assert result.error == "Search text cannot be empty."
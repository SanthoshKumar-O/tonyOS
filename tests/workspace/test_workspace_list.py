"""Tests for WorkspaceListTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools.workspace import WorkspaceListTool


def test_metadata() -> None:
    tool = WorkspaceListTool()

    assert tool.metadata.name == "workspace_list"


def test_lists_workspace_entries(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "README.md").touch()
    (tmp_path / "pyproject.toml").touch()

    monkeypatch.chdir(tmp_path)

    tool = WorkspaceListTool()

    result = tool.execute([])

    assert result.success is True
    assert "DIR\tsrc" in result.output
    assert "FILE\tREADME.md" in result.output
    assert "FILE\tpyproject.toml" in result.output


def test_directories_are_listed_before_files(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "z-file.txt").touch()
    (tmp_path / "a-directory").mkdir()
    (tmp_path / "a-file.txt").touch()

    monkeypatch.chdir(tmp_path)

    tool = WorkspaceListTool()

    result = tool.execute([])

    assert result.success is True

    lines = result.output.splitlines()

    assert lines[0] == "DIR\ta-directory"
    assert lines[1] == "FILE\ta-file.txt"
    assert lines[2] == "FILE\tz-file.txt"


def test_empty_workspace(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)

    tool = WorkspaceListTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == "Workspace is empty."
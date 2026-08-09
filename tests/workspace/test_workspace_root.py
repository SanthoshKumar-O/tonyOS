"""Tests for WorkspaceRootTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools.workspace import WorkspaceRootTool


def test_metadata() -> None:
    tool = WorkspaceRootTool()

    assert tool.metadata.name == "workspace_root"


def test_finds_current_directory_when_no_marker(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)

    tool = WorkspaceRootTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == str(tmp_path)


def test_finds_project_root(
    monkeypatch,
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    nested = project / "src"
    nested.mkdir(parents=True)

    (project / "pyproject.toml").touch()

    monkeypatch.chdir(nested)

    tool = WorkspaceRootTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == str(project)
"""Tests for WorkspaceInfoTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools.workspace import WorkspaceInfoTool


def test_metadata() -> None:
    tool = WorkspaceInfoTool()

    assert tool.metadata.name == "workspace_info"


def test_returns_workspace_information(
    monkeypatch,
    tmp_path: Path,
) -> None:
    project = tmp_path / "project"
    project.mkdir()

    (project / "pyproject.toml").touch()
    (project / "README.md").touch()
    (project / "src").mkdir()

    monkeypatch.chdir(project)

    tool = WorkspaceInfoTool()

    result = tool.execute([])

    assert result.success is True
    assert f"Path: {project}" in result.output
    assert f"Root: {project}" in result.output
    assert "Project types: Python" in result.output
    assert "Directories: 1" in result.output
    assert "Files: 2" in result.output


def test_empty_workspace(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)

    tool = WorkspaceInfoTool()

    result = tool.execute([])

    assert result.success is True
    assert f"Path: {tmp_path}" in result.output
    assert f"Root: {tmp_path}" in result.output
    assert "No known project types detected." in result.output
    assert "Directories: 0" in result.output
    assert "Files: 0" in result.output
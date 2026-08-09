"""Tests for ProjectDetectTool."""

from __future__ import annotations

from pathlib import Path

from tony.tools.workspace import ProjectDetectTool


def test_metadata() -> None:
    tool = ProjectDetectTool()

    assert tool.metadata.name == "project_detect"


def test_detects_python_project(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").touch()

    monkeypatch.chdir(tmp_path)

    tool = ProjectDetectTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == "Python"


def test_detects_multiple_project_types(
    monkeypatch,
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / "Dockerfile").touch()

    monkeypatch.chdir(tmp_path)

    tool = ProjectDetectTool()

    result = tool.execute([])

    assert result.success is True
    assert "Python" in result.output
    assert "Git" in result.output
    assert "Docker" in result.output


def test_no_project_detected(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)

    tool = ProjectDetectTool()

    result = tool.execute([])

    assert result.success is True
    assert result.output == "No known project types detected."
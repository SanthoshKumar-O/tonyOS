"""Tests for DockerRunTool."""

from __future__ import annotations

from tony.tools.docker import DockerRunTool


def test_metadata() -> None:
    tool = DockerRunTool()

    assert tool.metadata.name == "docker_run"
    assert tool.metadata.capability.value == "shell"


def test_requires_image() -> None:
    tool = DockerRunTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Docker image name is required."

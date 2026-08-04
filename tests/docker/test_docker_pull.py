"""Tests for DockerPullTool."""

from __future__ import annotations

from tony.tools.docker import DockerPullTool


def test_metadata() -> None:
    tool = DockerPullTool()

    assert tool.metadata.name == "docker_pull"
    assert tool.metadata.capability.value == "shell"


def test_requires_image_name() -> None:
    tool = DockerPullTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Docker image name is required."

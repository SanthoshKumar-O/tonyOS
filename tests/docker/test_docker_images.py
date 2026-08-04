"""Tests for DockerImagesTool."""

from __future__ import annotations

from tony.tools.docker import DockerImagesTool


def test_metadata() -> None:
    tool = DockerImagesTool()

    assert tool.metadata.name == "docker_images"
    assert tool.metadata.capability.value == "shell"


def test_execute_returns_result() -> None:
    tool = DockerImagesTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

"""Tests for DockerRmTool."""

from __future__ import annotations

from tony.tools.docker import DockerRmTool


def test_metadata() -> None:
    tool = DockerRmTool()

    assert tool.metadata.name == "docker_rm"
    assert tool.metadata.capability.value == "shell"


def test_requires_container() -> None:
    tool = DockerRmTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Container name or ID is required."

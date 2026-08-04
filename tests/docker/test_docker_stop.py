"""Tests for DockerStopTool."""

from __future__ import annotations

from tony.tools.docker import DockerStopTool


def test_metadata() -> None:
    tool = DockerStopTool()

    assert tool.metadata.name == "docker_stop"
    assert tool.metadata.capability.value == "shell"


def test_requires_container() -> None:
    tool = DockerStopTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Container name or ID is required."

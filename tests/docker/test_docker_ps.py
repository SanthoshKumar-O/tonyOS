"""Tests for DockerPsTool."""

from __future__ import annotations

from tony.tools.docker import DockerPsTool


def test_metadata() -> None:
    tool = DockerPsTool()

    assert tool.metadata.name == "docker_ps"
    assert tool.metadata.capability.value == "shell"


def test_execute_returns_result() -> None:
    tool = DockerPsTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

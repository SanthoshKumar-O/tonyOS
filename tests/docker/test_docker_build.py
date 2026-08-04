"""Tests for DockerBuildTool."""

from __future__ import annotations

from tony.tools.docker import DockerBuildTool


def test_metadata() -> None:
    tool = DockerBuildTool()

    assert tool.metadata.name == "docker_build"
    assert tool.metadata.capability.value == "shell"


def test_requires_build_context() -> None:
    tool = DockerBuildTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Build context is required."

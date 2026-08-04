"""Tests for the Docker registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.docker import DockerRegistry


def test_docker_registry_registers() -> None:
    registry = ToolRegistry()

    DockerRegistry.register(registry)

    assert registry.get("docker_ps").metadata.name == "docker_ps"
    assert registry.get("docker_images").metadata.name == "docker_images"
    assert registry.get("docker_pull").metadata.name == "docker_pull"
    assert registry.get("docker_run").metadata.name == "docker_run"
    assert registry.get("docker_stop").metadata.name == "docker_stop"
    assert registry.get("docker_rm").metadata.name == "docker_rm"
    assert registry.get("docker_build").metadata.name == "docker_build"

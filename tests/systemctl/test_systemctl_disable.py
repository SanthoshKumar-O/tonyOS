"""Tests for SystemctlDisableTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlDisableTool


def test_metadata() -> None:
    tool = SystemctlDisableTool()

    assert tool.metadata.name == "systemctl_disable"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlDisableTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

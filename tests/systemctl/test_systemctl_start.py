"""Tests for SystemctlStartTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlStartTool


def test_metadata() -> None:
    tool = SystemctlStartTool()

    assert tool.metadata.name == "systemctl_start"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlStartTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

"""Tests for SystemctlRestartTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlRestartTool


def test_metadata() -> None:
    tool = SystemctlRestartTool()

    assert tool.metadata.name == "systemctl_restart"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlRestartTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

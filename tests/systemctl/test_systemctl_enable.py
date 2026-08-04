"""Tests for SystemctlEnableTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlEnableTool


def test_metadata() -> None:
    tool = SystemctlEnableTool()

    assert tool.metadata.name == "systemctl_enable"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlEnableTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

"""Tests for SystemctlStopTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlStopTool


def test_metadata() -> None:
    tool = SystemctlStopTool()

    assert tool.metadata.name == "systemctl_stop"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlStopTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

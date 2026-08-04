"""Tests for SystemctlStatusTool."""

from __future__ import annotations

from tony.tools.systemctl import SystemctlStatusTool


def test_metadata() -> None:
    tool = SystemctlStatusTool()

    assert tool.metadata.name == "systemctl_status"
    assert tool.metadata.capability.value == "shell"


def test_requires_service_name() -> None:
    tool = SystemctlStatusTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Service name is required."

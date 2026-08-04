"""Tests for the systemctl registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.systemctl import SystemctlRegistry


def test_systemctl_registry_registers() -> None:
    registry = ToolRegistry()

    SystemctlRegistry.register(registry)

    assert registry is not None
    assert registry.get("systemctl_start").metadata.name == "systemctl_start"
    assert registry.get("systemctl_stop").metadata.name == "systemctl_stop"
    assert registry.get("systemctl_restart").metadata.name == "systemctl_restart"
    assert registry.get("systemctl_enable").metadata.name == "systemctl_enable"
    assert registry.get("systemctl_disable").metadata.name == "systemctl_disable"
    assert registry.get("systemctl_status").metadata.name == "systemctl_status"

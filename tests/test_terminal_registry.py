"""Tests for the terminal registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.terminal import TerminalRegistry


def test_terminal_registry_registers() -> None:
    registry = ToolRegistry()

    TerminalRegistry.register(registry)

    assert registry.get("execute").metadata.name == "execute"
    assert registry.get("process_list").metadata.name == "process_list"
    assert registry.get("kill_process").metadata.name == "kill_process"
    assert registry.get("whoami").metadata.name == "whoami"
    assert registry.get("hostname").metadata.name == "hostname"
    assert registry.get("uname").metadata.name == "uname"
    assert registry.get("date").metadata.name == "date"
    assert registry.get("uptime").metadata.name == "uptime"
    assert registry.get("environment").metadata.name == "environment"
    assert registry.get("disk_usage").metadata.name == "disk_usage"
    assert registry.get("memory_usage").metadata.name == "memory_usage"
    assert registry.get("cpu_info").metadata.name == "cpu_info"
    assert registry.get("os_info").metadata.name == "os_info"
    assert registry.get("ping").metadata.name == "ping"
    assert registry.get("ip_address").metadata.name == "ip_address"
    assert registry.get("network_interfaces").metadata.name == "network_interfaces"
    assert registry.get("which").metadata.name == "which"
    assert registry.get("history").metadata.name == "history"

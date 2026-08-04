"""Tests for NetworkInterfacesTool."""

from __future__ import annotations

from tony.tools.terminal import NetworkInterfacesTool


def test_metadata() -> None:
    tool = NetworkInterfacesTool()

    assert tool.metadata.name == "network_interfaces"


def test_execute() -> None:
    tool = NetworkInterfacesTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

"""Tests for IpAddressTool."""

from __future__ import annotations

from tony.tools.terminal import IpAddressTool


def test_metadata() -> None:
    tool = IpAddressTool()

    assert tool.metadata.name == "ip_address"


def test_execute() -> None:
    tool = IpAddressTool()

    result = tool.execute([])

    assert isinstance(result.success, bool)

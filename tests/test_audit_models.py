"""Tests for audit models."""

from __future__ import annotations

from tony.audit import AuditRecord


def test_audit_record() -> None:
    record = AuditRecord(
        tool="pwd",
        success=True,
        duration_ms=10.5,
    )

    assert record.tool == "pwd"
    assert record.success is True
    assert record.duration_ms == 10.5

"""Tests for the audit service."""

from __future__ import annotations

from tony.audit import (
    AuditRecord,
    AuditService,
)


def test_record() -> None:
    service = AuditService()

    record = AuditRecord(
        tool="pwd",
        success=True,
        duration_ms=5.0,
    )

    service.record(record)

    records = service.records()

    assert len(records) == 1
    assert records[0] == record


def test_clear() -> None:
    service = AuditService()

    service.record(
        AuditRecord(
            tool="pwd",
            success=True,
            duration_ms=1.0,
        ),
    )

    service.clear()

    assert service.records() == []


def test_records_returns_copy() -> None:
    service = AuditService()

    service.record(
        AuditRecord(
            tool="pwd",
            success=True,
            duration_ms=1.0,
        ),
    )

    records = service.records()

    records.clear()

    assert len(service.records()) == 1

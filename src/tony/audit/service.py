"""Audit service."""

from __future__ import annotations

from .models import AuditRecord
from .protocols import AuditServiceProtocol


class AuditService(AuditServiceProtocol):
    """Stores audit records."""

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def record(
        self,
        audit: AuditRecord,
    ) -> None:
        """Store an audit record."""

        self._records.append(audit)

    def records(
        self,
    ) -> list[AuditRecord]:
        """Return all audit records."""

        return list(self._records)

    def clear(
        self,
    ) -> None:
        """Remove all audit records."""

        self._records.clear()

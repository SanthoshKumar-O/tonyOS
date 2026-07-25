"""Audit protocols."""

from __future__ import annotations

from typing import Protocol

from .models import AuditRecord


class AuditServiceProtocol(Protocol):
    """Protocol for audit services."""

    def record(
        self,
        audit: AuditRecord,
    ) -> None: ...

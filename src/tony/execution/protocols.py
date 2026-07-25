"""Execution protocols."""

from __future__ import annotations

from typing import Protocol

from .models import ExecutionEvent


class ExecutionMonitorProtocol(Protocol):
    """Protocol for execution monitors."""

    def start(
        self,
        tool: str,
    ) -> ExecutionEvent: ...

    def complete(
        self,
        tool: str,
    ) -> ExecutionEvent: ...

    def fail(
        self,
        tool: str,
    ) -> ExecutionEvent: ...

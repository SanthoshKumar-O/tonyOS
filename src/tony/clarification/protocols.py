"""Protocols for the clarification system."""

from __future__ import annotations

from typing import Protocol

from tony.planner import ClarificationPlan

from .models import ClarificationRequest


class ClarificationEngineProtocol(Protocol):
    """Clarification engine interface."""

    def generate(
        self,
        plan: ClarificationPlan,
    ) -> ClarificationRequest: ...

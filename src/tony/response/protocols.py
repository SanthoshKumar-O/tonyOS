"""Protocols for the response system."""

from __future__ import annotations

from typing import Protocol

from tony.planner import ExecutionPlan

from .models import Response


class ResponseGeneratorProtocol(Protocol):
    """Response generator interface."""

    def generate(
        self,
        plan: ExecutionPlan,
    ) -> Response: ...

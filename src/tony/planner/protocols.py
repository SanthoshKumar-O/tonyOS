"""Protocols for the planner."""

from __future__ import annotations

from typing import Protocol

from tony.context import ExecutionContext
from tony.planner.models import ExecutionPlan


class PlannerProtocol(Protocol):
    """Planner interface."""

    def plan(
        self,
        context: ExecutionContext,
    ) -> ExecutionPlan: ...


class IntentClassifierProtocol(Protocol):
    """Intent classifier interface."""

    def classify(
        self,
        context: ExecutionContext,
    ) -> str: ...


class PlanFactoryProtocol(Protocol):
    """Plan factory interface."""

    def answer(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ExecutionPlan: ...

    def execute(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ExecutionPlan: ...

    def clarify(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ExecutionPlan: ...

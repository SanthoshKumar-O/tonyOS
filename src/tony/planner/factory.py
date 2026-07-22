"""Plan factory."""

from __future__ import annotations

from tony.planner.models import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
)


class PlanFactory:
    """Creates strongly typed execution plans."""

    def answer(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> AnswerPlan:
        """Create an answer plan."""

        return AnswerPlan(
            reason=reason,
            confidence=confidence,
        )

    def execute(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ExecutePlan:
        """Create an execution plan."""

        return ExecutePlan(
            reason=reason,
            confidence=confidence,
        )

    def clarify(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ClarificationPlan:
        """Create a clarification plan."""

        return ClarificationPlan(
            reason=reason,
            confidence=confidence,
        )

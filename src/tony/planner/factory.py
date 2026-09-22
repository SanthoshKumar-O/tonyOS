"""Plan factory."""

from __future__ import annotations

from tony.planner.models import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
)
from tony.tools.models import ToolArgument, ToolSelection


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
        selection: ToolSelection,
        arguments: list[ToolArgument] | None = None,
    ) -> ExecutePlan:
        """Create a tool execution plan."""

        return ExecutePlan(
            reason=reason,
            confidence=confidence,
            selection=selection,
            arguments=tuple(arguments or []),
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
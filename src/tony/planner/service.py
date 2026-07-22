"""Planner service."""

from __future__ import annotations

from tony.context import ExecutionContext
from tony.planner.models import ExecutionPlan
from tony.planner.protocols import (
    IntentClassifierProtocol,
    PlanFactoryProtocol,
    PlannerProtocol,
)


class PlannerService(PlannerProtocol):
    """Produces execution plans from an execution context."""

    def __init__(
        self,
        classifier: IntentClassifierProtocol,
        factory: PlanFactoryProtocol,
    ) -> None:
        self._classifier = classifier
        self._factory = factory

    def plan(
        self,
        context: ExecutionContext,
    ) -> ExecutionPlan:
        """Create an execution plan."""

        intent = self._classifier.classify(context)

        match intent:
            case "answer":
                return self._factory.answer(
                    reason="General question.",
                    confidence=1.0,
                )

            case "execute":
                return self._factory.execute(
                    reason="Tool execution required.",
                    confidence=1.0,
                )

            case "clarify":
                return self._factory.clarify(
                    reason="More information is required.",
                    confidence=1.0,
                )

        return self._factory.answer(
            reason="Unknown intent.",
            confidence=0.0,
        )

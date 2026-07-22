"""Response generator."""

from __future__ import annotations

from tony.planner import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
    ExecutionPlan,
)

from .exceptions import ResponseGenerationError
from .models import (
    AnswerResponse,
    ClarificationResponse,
    ExecutionResponse,
    Response,
)


class ResponseGenerator:
    """Converts execution plans into responses."""

    def generate(
        self,
        plan: ExecutionPlan,
    ) -> Response:
        """Generate a response from an execution plan."""

        if isinstance(plan, AnswerPlan):
            return AnswerResponse(
                content=plan.reason,
            )

        if isinstance(plan, ClarificationPlan):
            return ClarificationResponse(
                content=plan.reason,
            )

        if isinstance(plan, ExecutePlan):
            return ExecutionResponse(
                content=plan.reason,
            )

        raise ResponseGenerationError(f"Unsupported execution plan: {type(plan).__name__}")

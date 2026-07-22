from __future__ import annotations

import pytest

from tony.planner import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
    ExecutionPlan,
    PlanType,
)
from tony.response import (
    AnswerResponse,
    ClarificationResponse,
    ExecutionResponse,
    ResponseGenerationError,
    ResponseGenerator,
)


def test_generate_answer_response() -> None:
    generator = ResponseGenerator()

    plan = AnswerPlan(
        reason="Answer the user's question.",
        confidence=0.95,
    )

    response = generator.generate(plan)

    assert isinstance(response, AnswerResponse)
    assert response.content == "Answer the user's question."


def test_generate_execution_response() -> None:
    generator = ResponseGenerator()

    plan = ExecutePlan(
        reason="Execute git status.",
        confidence=0.90,
    )

    response = generator.generate(plan)

    assert isinstance(response, ExecutionResponse)
    assert response.content == "Execute git status."


def test_generate_clarification_response() -> None:
    generator = ResponseGenerator()

    plan = ClarificationPlan(
        reason="Which repository?",
        confidence=0.85,
    )

    response = generator.generate(plan)

    assert isinstance(response, ClarificationResponse)
    assert response.content == "Which repository?"


def test_unknown_plan_raises_error() -> None:
    generator = ResponseGenerator()

    class UnknownPlan(ExecutionPlan):
        plan_type: PlanType = PlanType.ANSWER

    plan = UnknownPlan(
        reason="Unknown",
        confidence=0.0,
    )

    with pytest.raises(ResponseGenerationError):
        generator.generate(plan)

from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.planner import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
    ExecutionPlan,
    PlanType,
)


def test_execution_plan() -> None:
    plan = ExecutionPlan(
        plan_type=PlanType.ANSWER,
        reason="General question.",
        confidence=0.95,
    )

    assert plan.plan_type is PlanType.ANSWER
    assert plan.reason == "General question."
    assert plan.confidence == 0.95


def test_answer_plan() -> None:
    plan = AnswerPlan(
        reason="Answer directly.",
        confidence=1.0,
    )

    assert plan.plan_type is PlanType.ANSWER
    assert isinstance(plan, ExecutionPlan)


def test_execute_plan() -> None:
    plan = ExecutePlan(
        reason="Execute a tool.",
        confidence=0.9,
    )

    assert plan.plan_type is PlanType.EXECUTE
    assert isinstance(plan, ExecutionPlan)


def test_clarification_plan() -> None:
    plan = ClarificationPlan(
        reason="Need more information.",
        confidence=0.8,
    )

    assert plan.plan_type is PlanType.CLARIFY
    assert isinstance(plan, ExecutionPlan)


def test_models_are_immutable() -> None:
    plan = AnswerPlan(
        reason="Immutable.",
        confidence=1.0,
    )

    with pytest.raises(ValidationError):
        plan.reason = "Changed"

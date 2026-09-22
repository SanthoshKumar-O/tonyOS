from __future__ import annotations

from tony.planner import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
    PlanFactory,
    PlanType,
)
from tony.tools import ToolSelection


def test_create_answer_plan() -> None:
    factory = PlanFactory()

    plan = factory.answer(
        reason="General question.",
        confidence=0.95,
    )

    assert isinstance(plan, AnswerPlan)
    assert plan.plan_type is PlanType.ANSWER
    assert plan.reason == "General question."
    assert plan.confidence == 0.95


def test_create_execute_plan() -> None:
    factory = PlanFactory()

    selection = ToolSelection(
        tool_name="ls",
        confidence=0.90,
        reason="List directory contents.",
    )

    plan = factory.execute(
        reason="Filesystem operation.",
        confidence=0.90,
        selection=selection,
    )

    assert isinstance(plan, ExecutePlan)
    assert plan.plan_type is PlanType.EXECUTE
    assert plan.reason == "Filesystem operation."
    assert plan.confidence == 0.90
    assert plan.selection == selection


def test_create_clarification_plan() -> None:
    factory = PlanFactory()

    plan = factory.clarify(
        reason="Need repository name.",
        confidence=0.80,
    )

    assert isinstance(plan, ClarificationPlan)
    assert plan.plan_type is PlanType.CLARIFY
    assert plan.reason == "Need repository name."
    assert plan.confidence == 0.80


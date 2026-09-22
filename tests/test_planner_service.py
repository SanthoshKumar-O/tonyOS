from __future__ import annotations

from tony.context import (
    EnvironmentContext,
    ExecutionContext,
    ExecutionMetadata,
    ExecutionSettings,
    RequestContext,
)
from tony.conversation import Conversation
from tony.planner import (
    AnswerPlan,
    ClarificationPlan,
    ExecutePlan,
    PlannerService,
)
from tony.session import Session
from tony.tools import ToolSelection

class DummyClassifier:
    """Dummy intent classifier."""

    def __init__(self, intent: str) -> None:
        self._intent = intent

    def classify(self, context: ExecutionContext) -> str:
        return self._intent

class DummySelector:
    def select(self, context: ExecutionContext) -> ToolSelection:
        return ToolSelection(
            tool_name="pwd",
            confidence=1.0,
            reason="Test selection",
        )
    
class DummyFactory:
    """Dummy plan factory."""

    def answer(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> AnswerPlan:
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
    ) -> ExecutePlan:
        return ExecutePlan(
            reason=reason,
            confidence=confidence,
            selection=selection,
        )

    def clarify(
        self,
        *,
        reason: str,
        confidence: float,
    ) -> ClarificationPlan:
        return ClarificationPlan(
            reason=reason,
            confidence=confidence,
        )


def create_context() -> ExecutionContext:
    return ExecutionContext(
        session=Session(),
        conversation=Conversation(),
        request=RequestContext(
            user_input="Hello",
        ),
        environment=EnvironmentContext(
            current_working_directory="/home/santhoshkumar",
            platform="linux",
            hostname="fedora",
            python_version="3.14",
        ),
        metadata=ExecutionMetadata(),
        settings=ExecutionSettings(
            provider_name="ollama",
            temperature=0.0,
            streaming=False,
        ),
    )


def test_execute_plan() -> None:
    planner = PlannerService(
    classifier=DummyClassifier("execute"),
    factory=DummyFactory(),
    selector=DummySelector(),
)

    plan = planner.plan(create_context())

    assert isinstance(plan, ExecutePlan)
    assert plan.selection.tool_name == "pwd"

def test_execute_plan() -> None:
    planner = PlannerService(
        classifier=DummyClassifier("execute"),
        factory=DummyFactory(),
        selection=DummySelector(),
    )

    plan = planner.plan(create_context())

    assert isinstance(plan, ExecutePlan)


def test_clarification_plan() -> None:
    planner = PlannerService(
        classifier=DummyClassifier("clarify"),
        factory=DummyFactory(),
        selection=DummySelector(),
    )

    plan = planner.plan(create_context())

    assert isinstance(plan, ClarificationPlan)


def test_unknown_intent_defaults_to_answer() -> None:
    planner = PlannerService(
        classifier=DummyClassifier("unknown"),
        factory=DummyFactory(),
        selection=DummySelector(),
    )

    plan = planner.plan(create_context())

    assert isinstance(plan, AnswerPlan)
    assert plan.confidence == 0.0

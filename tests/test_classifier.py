from __future__ import annotations

from tony.context import (
    EnvironmentContext,
    ExecutionContext,
    ExecutionMetadata,
    ExecutionSettings,
    RequestContext,
)
from tony.conversation import Conversation, Message, MessageRole
from tony.planner import IntentClassifier, PlanType
from tony.session import Session


def create_context(message: str | None = None) -> ExecutionContext:
    conversation = Conversation()

    if message is not None:
        conversation = conversation.add(
            Message(
                role=MessageRole.USER,
                content=message,
            )
        )

    return ExecutionContext(
        session=Session(),
        conversation=conversation,
        request=RequestContext(
            user_input=message or "",
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


def test_empty_conversation_returns_answer() -> None:
    classifier = IntentClassifier()

    plan = classifier.classify(create_context())

    assert plan is PlanType.ANSWER


def test_execute_intent() -> None:
    classifier = IntentClassifier()

    plan = classifier.classify(create_context("git commit -m 'Initial commit'"))

    assert plan is PlanType.EXECUTE


def test_clarify_intent() -> None:
    classifier = IntentClassifier()

    plan = classifier.classify(create_context("Which repository should I use?"))

    assert plan is PlanType.CLARIFY


def test_normal_question_returns_answer() -> None:
    classifier = IntentClassifier()

    plan = classifier.classify(create_context("Explain Python decorators."))

    assert plan is PlanType.ANSWER

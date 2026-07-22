from __future__ import annotations

from tony.context import (
    EnvironmentContext,
    ExecutionContext,
    ExecutionMetadata,
    ExecutionSettings,
    RequestContext,
)
from tony.context_builder import ContextBuilder
from tony.conversation import Conversation
from tony.prompts.builder import PromptBuilder
from tony.prompts.models import Prompt
from tony.session import Session


class DummyPromptManager:
    def get(self, name: str) -> Prompt:
        return Prompt(
            name="system",
            content="You are Tony.",
        )


def test_build_context() -> None:
    builder = ContextBuilder(
        prompt_manager=DummyPromptManager(),
        prompt_builder=PromptBuilder(
            DummyPromptManager(),
        ),
    )

    context = ExecutionContext(
        session=Session(),
        conversation=Conversation(),
        request=RequestContext(
            user_input="Hello",
        ),
        environment=EnvironmentContext(
            current_working_directory="/tmp",
            platform="linux",
            hostname="tony",
            python_version="3.14",
        ),
        metadata=ExecutionMetadata(),
        settings=ExecutionSettings(
            provider_name="ollama",
            temperature=0.2,
            streaming=False,
        ),
    )

    result = builder.build(context)

    assert "You are Tony." in result.prompt

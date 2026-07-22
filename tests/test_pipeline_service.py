from __future__ import annotations

from tony.clarification import ClarificationEngine
from tony.context import (
    EnvironmentContext,
    ExecutionContext,
    ExecutionMetadata,
    ExecutionSettings,
    RequestContext,
)
from tony.context_builder import ContextBuilder
from tony.conversation import Conversation
from tony.pipeline import IntelligencePipeline
from tony.planner import (
    IntentClassifier,
    PlanFactory,
    PlannerService,
)
from tony.prompts import (
    Prompt,
    PromptBuilder,
)
from tony.response import ResponseGenerator
from tony.session import Session
from tony.streaming import (
    ResponseStreamer,
    StreamData,
)


class DummyPromptManager:
    """Dummy prompt manager."""

    def get(
        self,
        name: str,
    ) -> Prompt:
        return Prompt(
            name=name,
            content="{conversation}",
        )


def test_pipeline_execute() -> None:
    prompt_manager = DummyPromptManager()

    pipeline = IntelligencePipeline(
        context_builder=ContextBuilder(
            prompt_manager=prompt_manager,
            prompt_builder=PromptBuilder(
                prompt_manager,
            ),
        ),
        planner=PlannerService(
            classifier=IntentClassifier(),
            factory=PlanFactory(),
        ),
        clarification_engine=ClarificationEngine(),
        response_generator=ResponseGenerator(),
        response_streamer=ResponseStreamer(),
    )

    context = ExecutionContext(
        session=Session(),
        conversation=Conversation(),
        request=RequestContext(
            user_input="Hello Tony",
        ),
        environment=EnvironmentContext(
            current_working_directory="/tmp",
            platform="Linux",
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

    chunks = list(pipeline.execute(context))

    assert len(chunks) == 3

    data = chunks[1]

    assert isinstance(
        data,
        StreamData,
    )

    assert data.content == "General question."

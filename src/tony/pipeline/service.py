"""Tony's intelligence pipeline."""

from __future__ import annotations

from collections.abc import Iterator

from tony.clarification import (
    ClarificationEngineProtocol,
)
from tony.context import ExecutionContext
from tony.context_builder import (
    ContextBuilderProtocol,
)
from tony.planner import (
    ClarificationPlan,
    PlannerProtocol,
)
from tony.response import (
    ResponseGeneratorProtocol,
)
from tony.streaming import (
    ResponseStreamerProtocol,
    StreamChunk,
)


class IntelligencePipeline:
    """Coordinates Tony's intelligence pipeline."""

    def __init__(
        self,
        *,
        context_builder: ContextBuilderProtocol,
        planner: PlannerProtocol,
        clarification_engine: ClarificationEngineProtocol,
        response_generator: ResponseGeneratorProtocol,
        response_streamer: ResponseStreamerProtocol,
    ) -> None:
        self._context_builder = context_builder
        self._planner = planner
        self._clarification_engine = clarification_engine
        self._response_generator = response_generator
        self._response_streamer = response_streamer

    def execute(
        self,
        context: ExecutionContext,
    ) -> Iterator[StreamChunk]:
        """Execute Tony's complete intelligence pipeline."""

        # Build prompt (currently unused, future planner input)
        self._context_builder.build(context)

        plan = self._planner.plan(
            context,
        )

        if isinstance(plan, ClarificationPlan):
            request = self._clarification_engine.generate(
                plan,
            )

            plan = ClarificationPlan(
                reason=request.question,
                confidence=plan.confidence,
            )

        response = self._response_generator.generate(
            plan,
        )

        return self._response_streamer.stream(
            response,
        )

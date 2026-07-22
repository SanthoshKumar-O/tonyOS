"""Execution Context Builder."""

from __future__ import annotations

from tony.context.models import ExecutionContext
from tony.context_builder.exceptions import ContextBuildError
from tony.context_builder.models import PromptBuildResult
from tony.prompts.protocols import (
    PromptBuilderProtocol,
    PromptManagerProtocol,
)


class ContextBuilder:
    """Builds the final LLM prompt from an ExecutionContext."""

    def __init__(
        self,
        prompt_manager: PromptManagerProtocol,
        prompt_builder: PromptBuilderProtocol,
    ) -> None:
        self._prompt_manager = prompt_manager
        self._prompt_builder = prompt_builder

    def build(
        self,
        context: ExecutionContext,
    ) -> PromptBuildResult:
        """Build the final prompt."""

        try:
            prompt = self._prompt_builder.build(
                conversation=context.conversation,
            )

            return PromptBuildResult(
                prompt=prompt,
            )

        except Exception as exc:
            raise ContextBuildError("Failed to build execution context.") from exc

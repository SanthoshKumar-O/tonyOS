"""Execution context service."""

from __future__ import annotations

from tony.context.models import (
    EnvironmentContext,
    ExecutionContext,
    ExecutionMetadata,
    ExecutionSettings,
    RequestContext,
)
from tony.conversation import Conversation
from tony.memory import MemoryRetriever
from tony.session import Session


class ExecutionContextService:
    """Creates immutable execution contexts."""

    def __init__(
        self,
        memory_retriever: MemoryRetriever | None = None,
    ) -> None:
        """Create the execution context service."""
        self._memory_retriever = memory_retriever

    def create(
        self,
        *,
        session: Session,
        conversation: Conversation,
        user_input: str,
        environment: EnvironmentContext,
        settings: ExecutionSettings,
    ) -> ExecutionContext:
        """Create a new execution context."""

        retrieved_memories = ()

        if self._memory_retriever is not None:
            retrieved_memories = tuple(
                self._memory_retriever.retrieve(user_input)
            )

        return ExecutionContext(
            session=session,
            conversation=conversation,
            request=RequestContext(
                user_input=user_input,
            ),
            environment=environment,
            metadata=ExecutionMetadata(),
            settings=settings,
            retrieved_memories=retrieved_memories,
        )

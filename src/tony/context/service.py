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
from tony.session import Session


class ExecutionContextService:
    """Creates immutable execution contexts."""

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

        return ExecutionContext(
            session=session,
            conversation=conversation,
            request=RequestContext(
                user_input=user_input,
            ),
            environment=environment,
            metadata=ExecutionMetadata(),
            settings=settings,
        )

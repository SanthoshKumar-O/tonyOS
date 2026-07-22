"""Conversation orchestration service."""

from __future__ import annotations

from tony.conversation.models import Conversation, Message, MessageRole
from tony.llm.protocols import LLMServiceProtocol
from tony.prompts.protocols import PromptBuilderProtocol


class ConversationService:
    """Coordinates conversations with the language model."""

    def __init__(
        self,
        prompt_builder: PromptBuilderProtocol,
        llm_service: LLMServiceProtocol,
    ) -> None:
        self._prompt_builder = prompt_builder
        self._llm_service = llm_service

    def reply(
        self,
        conversation: Conversation,
        user_message: str,
    ) -> Conversation:
        """Generate an assistant reply and return an updated conversation."""

        conversation = conversation.add(
            Message(
                role=MessageRole.USER,
                content=user_message,
            )
        )

        prompt = self._prompt_builder.build(conversation)

        response = self._llm_service.generate(prompt)

        conversation = conversation.add(
            Message(
                role=MessageRole.ASSISTANT,
                content=response,
            )
        )

        return conversation

"""Tony command-line interface."""

from __future__ import annotations

from tony.container import TonyContainer
from tony.conversation import Conversation
from tony.core.application import TonyApplication
from tony.core.bootstrap import ApplicationBootstrap
from tony.metadata import APPLICATION_METADATA


def run() -> None:
    """Run the interactive Tony CLI."""
    container = TonyContainer()

    application = TonyApplication(APPLICATION_METADATA)
    bootstrap = ApplicationBootstrap(application)

    provider = container.providers.get("ollama")

    provider.initialize()
    container.llm_service.initialize()

    bootstrap.startup()

    conversation = Conversation()

    print(f"{APPLICATION_METADATA.name} v{APPLICATION_METADATA.version}")
    print("Type /quit to exit.")

    try:
        while True:
            try:
                user_input = input("You: ")
            except EOFError:
                break

            if user_input.strip() == "/quit":
                break

            if not user_input.strip():
                continue

            conversation = container.conversation_service.reply(
                conversation,
                user_input,
            )

            response = conversation.last_message()

            if response is not None:
                print(f"Tony: {response.content}")
    except KeyboardInterrupt:
        print()
    finally:
        provider.shutdown()
        bootstrap.shutdown()


def main() -> None:
    """CLI entry point."""
    run()

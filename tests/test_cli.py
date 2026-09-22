from __future__ import annotations

from unittest.mock import MagicMock, patch

from tony.cli.app import run


def test_cli_exits_with_quit() -> None:
    provider = MagicMock()
    llm_service = MagicMock()

    with (
        patch("tony.cli.app.TonyContainer") as container_class,
        patch("tony.cli.app.TonyApplication"),
        patch("tony.cli.app.ApplicationBootstrap") as bootstrap_class,
        patch("tony.cli.app.input", return_value="/quit"),
    ):
        container = container_class.return_value
        container.providers.get.return_value = provider
        container.llm_service = llm_service

        run()

    provider.initialize.assert_called_once()
    llm_service.initialize.assert_called_once()
    provider.shutdown.assert_called_once()

    bootstrap_class.return_value.startup.assert_called_once()
    bootstrap_class.return_value.shutdown.assert_called_once()


def test_cli_sends_user_message_to_conversation_service() -> None:
    provider = MagicMock()
    llm_service = MagicMock()

    conversation_service = MagicMock()

    conversation = MagicMock()
    conversation.last_message.return_value.content = "Hello from Tony."

    conversation_service.reply.return_value = conversation

    with (
        patch("tony.cli.app.TonyContainer") as container_class,
        patch("tony.cli.app.TonyApplication"),
        patch("tony.cli.app.ApplicationBootstrap"),
        patch("tony.cli.app.input", side_effect=["hello", "/quit"]),
    ):
        container = container_class.return_value
        container.providers.get.return_value = provider
        container.llm_service = llm_service
        container.conversation_service = conversation_service

        run()

    conversation_service.reply.assert_called_once()

    args = conversation_service.reply.call_args.args

    assert args[1] == "hello"


def test_cli_ask_uses_intelligence_pipeline() -> None:
    provider = MagicMock()
    pipeline = MagicMock()

    chunk = MagicMock()
    chunk.content = "Pipeline response."
    pipeline.execute.return_value = iter([chunk])

    with (
        patch("tony.cli.app.TonyContainer") as container_class,
        patch("tony.cli.app.TonyApplication"),
        patch("tony.cli.app.ApplicationBootstrap") as bootstrap_class,
    ):
        container = container_class.return_value
        container.providers.get.return_value = provider
        container.intelligence_pipeline = pipeline

        session = MagicMock()
        session.conversation = MagicMock()

        container.session_manager.create.return_value = session

        container.context_service.create.return_value = MagicMock()

        from tony.cli.app import run

        run(["ask", "Hello Tony"])

    container.context_service.create.assert_called_once()
    pipeline.execute.assert_called_once()

    context = pipeline.execute.call_args.args[0]

    assert context is container.context_service.create.return_value

    provider.initialize.assert_called_once()
    provider.shutdown.assert_called_once()
    bootstrap_class.return_value.startup.assert_called_once()
    bootstrap_class.return_value.shutdown.assert_called_once()

"""Tony command-line interface."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from uuid import UUID

from tony.container import TonyContainer
from tony.context import (
    EnvironmentContext,
    ExecutionSettings,
)
from tony.core.application import TonyApplication
from tony.core.bootstrap import ApplicationBootstrap
from tony.memory import Memory, MemoryScope
from tony.metadata import APPLICATION_METADATA


def create_parser() -> argparse.ArgumentParser:
    """Create the Tony command-line parser."""
    parser = argparse.ArgumentParser(
        prog="tony",
        description="Tony - a local-first AI system administrator for Fedora Linux.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser(
        "chat",
        help="Start an interactive chat session.",
    )

    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask Tony a single question.",
    )
    ask_parser.add_argument(
        "prompt",
        help="Question or instruction for Tony.",
    )

    memory_parser = subparsers.add_parser(
        "memory",
        help="Manage Tony's memory.",
    )

    memory_subparsers = memory_parser.add_subparsers(
        dest="memory_command",
    )

    memory_subparsers.add_parser(
        "list",
        help="List Tony memories.",
    )

    create_memory_parser = memory_subparsers.add_parser(
        "create",
        help="Create a Tony memory.",
    )
    create_memory_parser.add_argument(
        "scope",
        help="Memory scope.",
        choices=("working", "conversation", "project", "workspace", "semantic"),
    )
    create_memory_parser.add_argument(
        "content",
        help="Memory content.",
    )

    forget_memory_parser = memory_subparsers.add_parser(
        "forget",
        help="Forget a Tony memory.",
    )
    forget_memory_parser.add_argument(
        "memory_id",
        help="ID of the memory to forget.",
    )

    session_parser = subparsers.add_parser(
        "session",
        help="Manage Tony sessions.",
    )

    session_subparsers = session_parser.add_subparsers(
        dest="session_command",
    )

    session_subparsers.add_parser(
        "list",
        help="List Tony sessions.",
    )

    create_session_parser = session_subparsers.add_parser(
        "create",
        help="Create a new Tony session.",
    )
    create_session_parser.add_argument(
        "title",
        help="Session title.",
    )

    delete_session_parser = session_subparsers.add_parser(
        "delete",
        help="Delete a Tony session.",
    )
    delete_session_parser.add_argument(
        "session_id",
        help="ID of the session to delete.",
    )

    use_session_parser = session_subparsers.add_parser(
        "use",
        help="Set the active Tony session.",
    )
    use_session_parser.add_argument(
        "session_id",
        help="ID of the session to activate.",
    )

    subparsers.add_parser(
        "tools",
        help="Inspect Tony tools.",
    )

    subparsers.add_parser(
        "config",
        help="Inspect Tony configuration.",
    )

    subparsers.add_parser(
        "status",
        help="Show Tony system status.",
    )

    subparsers.add_parser(
        "diagnostics",
        help="Run Tony diagnostics.",
    )

    return parser


class CLIApplication:
    """Interface-layer application for Tony."""

    def __init__(self, container: TonyContainer) -> None:
        self._container = container

    def run_chat(self) -> None:
        """Run an interactive chat session."""
        provider = self._container.providers.get("ollama")

        application = TonyApplication(APPLICATION_METADATA)
        bootstrap = ApplicationBootstrap(application)

        provider.initialize()
        self._container.llm_service.initialize()
        bootstrap.startup()

        session_manager = self._container.session_manager

        try:
            try:
                session = session_manager.active()
            except Exception:
                session = session_manager.create("Tony Chat")

            print(f"{APPLICATION_METADATA.name} v{APPLICATION_METADATA.version}")
            print(f"Session: {session.title}")
            print("Type /quit to exit.")

            while True:
                try:
                    user_input = input("You: ")
                except EOFError:
                    break

                if user_input.strip() == "/quit":
                    break

                if not user_input.strip():
                    continue

                conversation = self._container.conversation_service.reply(
                    session.conversation,
                    user_input,
                )

                session = session_manager.update_conversation(
                    session.id,
                    conversation,
                )

                response = session.conversation.last_message()

                if response is not None:
                    print(f"Tony: {response.content}")

        except KeyboardInterrupt:
            print()
        finally:
            provider.shutdown()
            bootstrap.shutdown()

    def run_tools(self) -> None:
        """List registered Tony tools."""
        print("Tony Tools")

        for tool in self._container.tool_registry.tools():
            metadata = tool.metadata
            print(f"{metadata.name:<24} {metadata.capability.value:<12} {metadata.description}")

    def run_memory_list(self) -> None:
        """List Tony memories."""
        for memory in self._container.memory_manager.recall():
            print(f"{memory.id}  {memory.scope.value}  {memory.content}")

    def run_memory_create(
        self,
        scope: str,
        content: str,
    ) -> None:
        """Create a Tony memory."""
        provider = self._container.providers.get("ollama")

        if provider is None:
            raise RuntimeError("Ollama provider is not registered.")

        provider.initialize()

        try:
            memory = Memory(
                content=content,
                scope=MemoryScope(scope),
            )

            self._container.memory_manager.remember(memory)

            print(f"{memory.id}  {memory.scope.value}  {memory.content}")

        finally:
            provider.shutdown()

    def run_memory_forget(self, memory_id: str) -> None:
        """Forget a Tony memory."""
        self._container.memory_manager.forget(UUID(memory_id))
        print(f"Forgot memory: {memory_id}")

    def run_config(self) -> None:
        """Show Tony configuration."""
        configuration = self._container.configuration

        print("Tony Configuration")
        print(f"application.name: {configuration.application.name}")
        print(f"application.environment: {configuration.application.environment}")
        print(f"logging.level: {configuration.logging.level.value}")
        print(f"ollama.host: {configuration.ollama.host}")
        print(f"ollama.model: {configuration.ollama.model}")
        print(f"ollama.embedding_model: {configuration.ollama.embedding_model}")
        print(f"ollama.timeout: {configuration.ollama.timeout}")
        print(f"persistence.database_path: {configuration.persistence.database_path}")

    def run_status(self) -> None:
        """Show Tony system status."""
        configuration = self._container.configuration
        provider = self._container.providers.get("ollama")

        print(f"Tony v{APPLICATION_METADATA.version}")
        print(f"Environment: {configuration.application.environment}")
        print(f"Provider: {provider.name}")
        print(f"Provider initialized: {provider.initialized}")
        print(f"LLM initialized: {self._container.llm_service.initialized}")
        print("Persistence: available")
        print(f"Tools registered: {len(self._container.tool_registry.tools())}")
        print(f"Memory store: available")
        print(f"Database: {configuration.persistence.database_path}")

    def run_diagnostics(self) -> None:
        """Run Tony diagnostics."""
        configuration = self._container.configuration
        provider = self._container.providers.get("ollama")

        print("Tony Diagnostics")

        print("Configuration: OK")

        try:
            persistence = self._container.persistence
            persistence.connection.execute("SELECT 1")
            print("Persistence: OK")
        except Exception as exc:
            print(f"Persistence: FAILED ({exc})")

        print(f"Provider registered: {'OK' if provider is not None else 'FAILED'}")

        if provider is None:
            print("Ollama health: FAILED (provider not registered)")
        else:
            try:
                provider.initialize()
                try:
                    if provider.health():
                        print("Ollama health: OK")
                    else:
                        print("Ollama health: FAILED")
                finally:
                    provider.shutdown()
            except Exception as exc:
                print(f"Ollama health: FAILED ({exc})")

        try:
            tool_count = len(self._container.tool_registry.tools())
            print(f"Tools: OK ({tool_count} registered)")
        except Exception as exc:
            print(f"Tools: FAILED ({exc})")

        try:
            self._container.memory_store
            print("Memory store: OK")
        except Exception as exc:
            print(f"Memory store: FAILED ({exc})")

        print(f"Database: {configuration.persistence.database_path}")

    def route(self, args: argparse.Namespace) -> None:
        """Route parsed CLI arguments to the appropriate command handler."""
        if args.command == "ask":
            self.run_ask(args.prompt)
            return

        if args.command == "tools":
            self.run_tools()
            return

        if args.command == "memory":
            self._route_memory(args)
            return

        if args.command == "session":
            self._route_session(args)
            return

        if args.command == "config":
            self.run_config()
            return

        if args.command == "status":
            self.run_status()
            return

        if args.command == "diagnostics":
            self.run_diagnostics()
            return

        self.run_chat()

    def _route_memory(self, args: argparse.Namespace) -> None:
        """Route memory subcommands."""
        if args.memory_command == "list":
            self.run_memory_list()
            return

        if args.memory_command == "create":
            self.run_memory_create(
                args.scope,
                args.content,
            )
            return

        if args.memory_command == "forget":
            self.run_memory_forget(args.memory_id)
            return

    def _route_session(self, args: argparse.Namespace) -> None:
        """Route session subcommands."""
        session_manager = self._container.session_manager

        if args.session_command == "list":
            for session in session_manager.list():
                print(f"{session.id}  {session.title}")
            return

        if args.session_command == "create":
            session = session_manager.create(args.title)
            print(f"{session.id}  {session.title}")
            return

        if args.session_command == "delete":
            session_manager.delete(UUID(args.session_id))
            print(f"Deleted session: {args.session_id}")
            return

        if args.session_command == "use":
            session_manager.set_active(UUID(args.session_id))
            print(f"Active session: {args.session_id}")
            return

    def run_ask(self, prompt: str) -> None:
        """Ask Tony a single question."""
        provider = self._container.providers.get("ollama")

        application = TonyApplication(APPLICATION_METADATA)
        bootstrap = ApplicationBootstrap(application)

        provider.initialize()
        self._container.llm_service.initialize()
        bootstrap.startup()

        try:
            session = self._container.session_manager.create(
                "Tony Ask",
            )

            context = self._container.context_service.create(
                session=session,
                conversation=session.conversation,
                user_input=prompt,
                environment=EnvironmentContext(
                    current_working_directory=str(
                        __import__("pathlib").Path.cwd(),
                    ),
                    platform=__import__("platform").system(),
                    hostname=__import__("socket").gethostname(),
                    python_version=__import__("platform").python_version(),
                ),
                settings=ExecutionSettings(
                    provider_name="ollama",
                    temperature=0.0,
                    streaming=False,
                ),
            )

            for chunk in self._container.intelligence_pipeline.execute(context):
                if chunk.content:
                    print(chunk.content)

        except KeyboardInterrupt:
            print()

        finally:
            provider.shutdown()
            bootstrap.shutdown()


def run(argv: Sequence[str] | None = None) -> None:
    """Run the Tony CLI."""
    parser = create_parser()
    args = parser.parse_args([] if argv is None else argv)

    container = TonyContainer()
    application = CLIApplication(container)

    application.route(args)


def main() -> None:
    """CLI entry point."""
    import sys

    run(sys.argv[1:])

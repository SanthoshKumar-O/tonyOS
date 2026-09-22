from __future__ import annotations

from unittest.mock import MagicMock, patch

from tony.cli.app import create_parser, run


def test_cli_exposes_m62_commands() -> None:
    parser = create_parser()

    args = parser.parse_args(["memory"])
    assert args.command == "memory"

    args = parser.parse_args(["session"])
    assert args.command == "session"

    args = parser.parse_args(["tools"])
    assert args.command == "tools"

    args = parser.parse_args(["config"])
    assert args.command == "config"

    args = parser.parse_args(["status"])
    assert args.command == "status"

    args = parser.parse_args(["diagnostics"])
    assert args.command == "diagnostics"

def test_cli_config(capsys) -> None:
    configuration = MagicMock()

    configuration.application.name = "Tony"
    configuration.application.environment = "development"
    configuration.logging.level.value = "INFO"
    configuration.ollama.host = "http://127.0.0.1:11434"
    configuration.ollama.model = "qwen3:8b"
    configuration.ollama.embedding_model = "nomic-embed-text:latest"
    configuration.ollama.timeout = 120
    configuration.persistence.database_path = "data/tony.db"

    with patch("tony.cli.app.TonyContainer") as container_class:
        container_class.return_value.configuration = configuration

        run(["config"])

    output = capsys.readouterr().out

    assert "Tony Configuration" in output
    assert "application.name: Tony" in output
    assert "application.environment: development" in output
    assert "logging.level: INFO" in output
    assert "ollama.model: qwen3:8b" in output
    assert "persistence.database_path: data/tony.db" in output


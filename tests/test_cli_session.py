from __future__ import annotations

from unittest.mock import MagicMock, patch
from uuid import uuid4

from tony.cli.app import run


def test_cli_session_list() -> None:
    session = MagicMock()
    session.id = uuid4()
    session.title = "Test Session"

    manager = MagicMock()
    manager.list.return_value = [session]

    with patch("tony.cli.app.TonyContainer") as container_class:
        container = container_class.return_value
        container.session_manager = manager

        run(["session", "list"])

    manager.list.assert_called_once()


def test_cli_session_create() -> None:
    manager = MagicMock()
    manager.create.return_value = MagicMock(
        id=uuid4(),
        title="My Chat",
    )

    with patch("tony.cli.app.TonyContainer") as container_class:
        container = container_class.return_value
        container.session_manager = manager

        run(["session", "create", "My Chat"])

    manager.create.assert_called_once_with("My Chat")


def test_cli_session_delete() -> None:
    session_id = uuid4()

    manager = MagicMock()

    with patch("tony.cli.app.TonyContainer") as container_class:
        container = container_class.return_value
        container.session_manager = manager

        run(["session", "delete", str(session_id)])

    manager.delete.assert_called_once_with(session_id)


def test_cli_session_use() -> None:
    session_id = uuid4()

    manager = MagicMock()

    with patch("tony.cli.app.TonyContainer") as container_class:
        container = container_class.return_value
        container.session_manager = manager

        run(["session", "use", str(session_id)])

    manager.set_active.assert_called_once_with(session_id)

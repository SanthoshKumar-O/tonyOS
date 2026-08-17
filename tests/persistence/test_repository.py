from __future__ import annotations

from tony.persistence import SessionRepository


def test_session_repository_defines_save() -> None:
    assert hasattr(SessionRepository, "save")


def test_session_repository_defines_get() -> None:
    assert hasattr(SessionRepository, "get")


def test_session_repository_defines_list() -> None:
    assert hasattr(SessionRepository, "list")


def test_session_repository_defines_delete() -> None:
    assert hasattr(SessionRepository, "delete")


def test_session_repository_defines_exists() -> None:
    assert hasattr(SessionRepository, "exists")
from tony.container import TonyContainer


def test_configuration_is_singleton() -> None:
    container = TonyContainer()

    assert container.configuration is container.configuration


def test_logger_is_singleton() -> None:
    container = TonyContainer()

    assert container.logger is container.logger


def test_persistence_is_singleton() -> None:
    container = TonyContainer()

    assert container.persistence is container.persistence


def test_session_repository_is_singleton() -> None:
    container = TonyContainer()

    assert container.session_repository is container.session_repository


def test_session_manager_is_singleton() -> None:
    container = TonyContainer()

    assert container.session_manager is container.session_manager


def test_session_repository_uses_container_persistence() -> None:
    container = TonyContainer()

    assert container.session_repository._persistence is container.persistence


def test_persistence_is_singleton() -> None:
    container = TonyContainer()

    assert container.persistence is container.persistence


def test_session_repository_is_singleton() -> None:
    container = TonyContainer()

    assert container.session_repository is container.session_repository


def test_session_repository_uses_container_persistence() -> None:
    container = TonyContainer()

    repository = container.session_repository

    assert repository._persistence is container.persistence


def test_session_repository_is_singleton() -> None:
    container = TonyContainer()

    assert container.session_repository is container.session_repository


def test_persistence_is_singleton() -> None:
    container = TonyContainer()

    assert container.persistence is container.persistence


def test_session_manager_uses_container_repository() -> None:
    container = TonyContainer()

    manager = container.session_manager

    assert manager._repository is container.session_repository


def test_session_repository_uses_container_persistence() -> None:
    container = TonyContainer()

    repository = container.session_repository

    assert repository._persistence is container.persistence


def test_container_session_persistence_round_trip() -> None:
    container = TonyContainer()

    session = container.session_manager.create("Container Test")

    loaded = container.session_repository.get(session.id)

    assert loaded == session


def test_providers_is_singleton() -> None:
    container = TonyContainer()

    assert container.providers is container.providers


def test_prompt_manager_is_singleton() -> None:
    container = TonyContainer()

    assert container.prompt_manager is container.prompt_manager


def test_prompt_builder_is_singleton() -> None:
    container = TonyContainer()

    assert container.prompt_builder is container.prompt_builder


def test_llm_service_is_singleton() -> None:
    container = TonyContainer()

    assert container.llm_service is container.llm_service


def test_conversation_service_is_singleton() -> None:
    container = TonyContainer()

    assert container.conversation_service is container.conversation_service


def test_prompt_builder_uses_container_prompt_manager() -> None:
    container = TonyContainer()

    assert container.prompt_builder._prompt_manager is container.prompt_manager


def test_llm_service_uses_container_provider_manager() -> None:
    container = TonyContainer()

    assert container.llm_service._provider_manager is container.providers


def test_conversation_service_uses_container_prompt_builder() -> None:
    container = TonyContainer()

    assert container.conversation_service._prompt_builder is container.prompt_builder


def test_conversation_service_uses_container_llm_service() -> None:
    container = TonyContainer()

    assert container.conversation_service._llm_service is container.llm_service

from __future__ import annotations

from unittest.mock import Mock

import pytest

from tony.llm.exceptions import (
    LLMGenerationError,
    LLMInitializationError,
)
from tony.llm.service import LLMService
from tony.providers.manager import ProviderManager


def make_provider() -> Mock:
    provider = Mock()
    provider.initialized = True
    provider.generate.return_value = "Hello Tony"
    return provider


def test_initialize() -> None:
    manager = ProviderManager()

    provider = make_provider()

    manager.register(provider)

    manager.get = Mock(return_value=provider)

    service = LLMService(manager)

    service.initialize()

    assert service.initialized


def test_generate() -> None:
    manager = ProviderManager()

    provider = make_provider()

    manager.get = Mock(return_value=provider)

    service = LLMService(manager)

    service.initialize()

    result = service.generate("Hello")

    assert result == "Hello Tony"


def test_generate_before_initialize() -> None:
    manager = ProviderManager()

    service = LLMService(manager)

    with pytest.raises(LLMInitializationError):
        service.generate("Hello")


def test_generation_error() -> None:
    manager = ProviderManager()

    provider = make_provider()

    provider.generate.side_effect = RuntimeError()

    manager.get = Mock(return_value=provider)

    service = LLMService(manager)

    service.initialize()

    with pytest.raises(LLMGenerationError):
        service.generate("Hello")

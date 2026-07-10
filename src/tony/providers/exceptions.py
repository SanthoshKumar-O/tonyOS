from __future__ import annotations


class ProviderError(RuntimeError):
    """Base exception for all provider-related errors."""


class ProviderInitializationError(ProviderError):
    """Raised when a provider fails to initialize."""


class ProviderAlreadyRegisteredError(ProviderError):
    """Raised when attempting to register an existing provider."""


class ProviderNotFoundError(ProviderError):
    """Raised when a requested provider is not registered."""

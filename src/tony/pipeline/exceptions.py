"""Exceptions for Tony's intelligence pipeline."""

from __future__ import annotations


class IntelligencePipelineError(Exception):
    """Base exception for the intelligence pipeline."""


class PipelineExecutionError(IntelligencePipelineError):
    """Raised when the intelligence pipeline cannot complete."""

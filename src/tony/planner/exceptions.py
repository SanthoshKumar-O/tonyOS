"""Exceptions for the planner."""

from __future__ import annotations


class PlannerError(Exception):
    """Base exception for planner errors."""


class PlanningError(PlannerError):
    """Raised when planning cannot be completed."""

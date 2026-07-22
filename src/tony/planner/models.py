"""Planner models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class PlanType(StrEnum):
    """Types of plans Tony can produce."""

    ANSWER = "answer"
    EXECUTE = "execute"
    CLARIFY = "clarify"


class ExecutionPlan(BaseModel):
    """Base execution plan."""

    model_config = ConfigDict(
        frozen=True,
    )

    plan_type: PlanType
    reason: str
    confidence: float


class AnswerPlan(ExecutionPlan):
    """Plan representing a direct response."""

    model_config = ConfigDict(
        frozen=True,
    )

    plan_type: PlanType = PlanType.ANSWER


class ExecutePlan(ExecutionPlan):
    """Plan representing tool execution."""

    model_config = ConfigDict(
        frozen=True,
    )

    plan_type: PlanType = PlanType.EXECUTE


class ClarificationPlan(ExecutionPlan):
    """Plan requesting additional information."""

    model_config = ConfigDict(
        frozen=True,
    )

    plan_type: PlanType = PlanType.CLARIFY

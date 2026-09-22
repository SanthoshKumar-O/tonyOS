"""Planner models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from tony.tools.models import ToolArgument, ToolSelection


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
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


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

    selection: ToolSelection
    arguments: tuple[ToolArgument, ...] = ()


class ClarificationPlan(ExecutionPlan):
    """Plan requesting additional information."""

    model_config = ConfigDict(
        frozen=True,
    )

    plan_type: PlanType = PlanType.CLARIFY
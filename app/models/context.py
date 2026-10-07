from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class MilestonePacket(BaseModel):
    title: str
    description: str | None = None
    order_index: int = Field(default=1, gt=0)
    priority: int = Field(default=1, ge=1, le=5)
    start_date: date | None = None
    deadline: date | None = None


class ProjectPacket(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)
    deadline: date | None = None


class TaskPacket(BaseModel):
    title: str
    description: str | None = None
    why: str | None = None
    definition_of_done: str | None = None

    priority: int = Field(default=1, ge=1, le=5)

    scheduled_date: date | None = None
    due_date: date | None = None

    estimated_minutes: int | None = Field(
        default=None,
        gt=0,
    )

    plan_order: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )

    milestone_index: int | None = None
    project_index: int | None = None


class MissionPacket(BaseModel):
    title: str
    description: str | None = None
    start_date: date
    deadline: date
    priority: int = Field(default=1, ge=1, le=5)


class DailyContextPacket(BaseModel):
    summary: str | None = None

    accomplishments: list[str] = Field(
        default_factory=list
    )

    unfinished_tasks: list[str] = Field(
        default_factory=list
    )

    blockers: list[str] = Field(
        default_factory=list
    )

    insights: list[str] = Field(
        default_factory=list
    )

    tomorrow_focus: list[str] = Field(
        default_factory=list
    )

    mood: str | None = None

    energy: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )


class HabitSignalPacket(BaseModel):
    habit_key: str
    value: bool
    notes: str | None = None


class ContextPacket(BaseModel):
    type: str

    user_id: UUID

    effective_date: date | None = None

    # Mission update/create
    mission_id: UUID | None = None
    mission: MissionPacket | None = None

    milestones: list[MilestonePacket] = Field(
        default_factory=list
    )

    projects: list[ProjectPacket] = Field(
        default_factory=list
    )

    tasks: list[TaskPacket] = Field(
        default_factory=list
    )

    # Nightly reflection
    daily_context: DailyContextPacket | None = None

    habit_signals: list[HabitSignalPacket] = Field(
        default_factory=list
    )

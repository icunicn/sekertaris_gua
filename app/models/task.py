from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    user_id: UUID

    milestone_id: UUID | None = None
    project_id: UUID | None = None

    title: str = Field(min_length=1, max_length=300)
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


class TaskUpdate(BaseModel):
    milestone_id: UUID | None = None
    project_id: UUID | None = None

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=300,
    )

    description: str | None = None
    why: str | None = None
    definition_of_done: str | None = None

    priority: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    status: str | None = None

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


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID

    milestone_id: UUID | None
    project_id: UUID | None

    title: str
    description: str | None
    why: str | None
    definition_of_done: str | None

    priority: int
    status: str

    scheduled_date: date | None
    due_date: date | None

    estimated_minutes: int | None
    plan_order: int | None

    completed_at: datetime | None

    created_at: datetime
    updated_at: datetime

class TodayProgressResponse(BaseModel):
    date: date
    total: int
    completed: int
    remaining: int
    completion_rate: float
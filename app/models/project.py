from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    mission_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)
    deadline: date | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    deadline: date | None = None
    status: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    mission_id: UUID
    title: str
    description: str | None
    priority: int
    status: str
    deadline: date | None
    created_at: datetime
    updated_at: datetime

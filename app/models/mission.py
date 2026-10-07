from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field


class MissionCreate(BaseModel):
    user_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    start_date: date
    deadline: date
    priority: int = Field(default=1, ge=1, le=5)


class MissionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    start_date: date | None = None
    deadline: date | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    status: str | None = None


class MissionResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    start_date: date
    deadline: date
    priority: int
    status: str
    created_at: datetime
    updated_at: datetime

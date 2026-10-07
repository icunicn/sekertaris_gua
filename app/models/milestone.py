from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime


class MilestoneCreate(BaseModel):
    mission_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    order_index: int = Field(default=1, gt=0)
    priority: int = Field(default=1, ge=1, le=5)
    start_date: date | None = None
    deadline: date | None = None


class MilestoneUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    order_index: int | None = Field(default=None, gt=0)
    priority: int | None = Field(default=None, ge=1, le=5)
    start_date: date | None = None
    deadline: date | None = None
    status: str | None = None


class MilestoneResponse(BaseModel):
    id: UUID
    mission_id: UUID
    title: str
    description: str | None
    order_index: int
    priority: int
    start_date: date | None
    deadline: date | None
    status: str
    created_at: datetime
    updated_at: datetime

from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel
from tasks_backend.utils.get_current_utc_time import get_current_utc_time


class Status(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(SQLModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    due_date: date | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: Status = Field(default=Status.NOT_STARTED)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(default_factory=get_current_utc_time)


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    due_date: date | None = None
    status: Status | None = None

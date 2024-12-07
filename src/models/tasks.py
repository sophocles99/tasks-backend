from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel
from utils import get_current_utc_time


class Status(Enum):
    done = "done"
    in_progess = "in_progress"
    not_done = "not_done"


class TaskBase(SQLModel):
    name: str
    description: str | None = None
    due_date: date | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: Status = Field(default=Status.not_done)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(default_factory=get_current_utc_time)


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime

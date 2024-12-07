from datetime import date, datetime
from enum import Enum

from sqlmodel import Field, SQLModel
from utils import get_current_utc_time


class TaskStatus(Enum):
    done = "done"
    in_progess = "in_progress"
    not_done = "not_done"


print("Defining TaskCreate")


class TaskCreate(SQLModel):
    name: str
    description: str | None = None
    due_date: date | None = None


print("Defining Task")


class Task(TaskCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.not_done)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(default_factory=get_current_utc_time)

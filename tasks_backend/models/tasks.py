from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import Field, Session, SQLModel, select

from tasks_backend.utils.utils import get_current_utc_time


class Status(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(SQLModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    due_date: date | None = None
    status: Status = Field(default=Status.NOT_STARTED)


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime | None = None


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: UUID
    user_id: UUID
    status: Status
    created_at: datetime
    updated_at: datetime | None


class TaskUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=500)
    due_date: date | None = None
    status: Status | None = None


def get_task_or_raise_404(user_id: UUID, task_id: UUID, session: Session) -> Task:
    try:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=404, detail="More than one task found")
    return task

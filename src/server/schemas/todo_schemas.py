from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class Todo(BaseModel):
    title: str
    description: str
    status: Literal['done', 'not done', 'in progress']
    created_at: datetime


class TodoUpdate(Todo):
    title: str | None
    description: str | None
    status: Literal['done', 'not done', 'in progress'] | None
    created_at: datetime | None

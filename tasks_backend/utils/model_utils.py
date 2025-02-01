from fastapi import HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import select

from tasks_backend.models.tasks import Task
from tasks_backend.models.users import User


def get_user_or_raise_404(user_id: int, session):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_task_or_raise_404(user_id, task_id, session):
    try:
        task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Task not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=404, detail="More than one task found")
    return task

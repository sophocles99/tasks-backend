from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.db import get_session
from tasks_backend.models.tasks import (
    Task,
    TaskCreate,
    TaskPublic,
    TaskUpdate,
    get_task_or_raise_404,
)
from tasks_backend.models.users import get_user_or_raise_404

router = APIRouter(prefix="/tasks")


@router.post("/{user_id}", response_model=TaskPublic)
def create_task(task_create: TaskCreate, user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = Task.model_validate(task_create, update={"user_id": user_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{user_id}", response_model=list[TaskPublic])
def read_tasks(user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.get("/{user_id}/{task_id}", response_model=TaskPublic)
def read_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    return task


@router.patch("/{user_id}/{task_id}", response_model=TaskPublic)
def update_task(
    user_id: UUID, task_id: UUID, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    task_update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/{task_id}")
def delete_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

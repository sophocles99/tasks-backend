from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.auth import get_current_user
from tasks_backend.database.db import get_session
from tasks_backend.models.categories import get_category_or_raise_404
from tasks_backend.models.tasks import Task, TaskCreate, TaskPublic, TaskUpdate, get_task_or_raise_404
from tasks_backend.models.users import User
from tasks_backend.utils.utils import get_current_utc_time

router = APIRouter(prefix="/tasks")


@router.post("", response_model=TaskPublic)
def create_task(
    task_create: TaskCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    if task_create.category_id is not None:
        get_category_or_raise_404(current_user.id, task_create.category_id, session)
    task = Task.model_validate(task_create, update={"user_id": current_user.id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("", response_model=list[TaskPublic])
def read_tasks(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return tasks


@router.get("/{task_id}", response_model=TaskPublic)
def read_task(task_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = get_task_or_raise_404(current_user.id, task_id, session)
    return task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    task = get_task_or_raise_404(current_user.id, task_id, session)
    task_update_data = task_update.model_dump(exclude_unset=True)
    if task_update_data.get("category_id") is not None:
        get_category_or_raise_404(current_user.id, task_update_data["category_id"], session)
    task.sqlmodel_update(task_update_data)
    task.updated_at = get_current_utc_time()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = get_task_or_raise_404(current_user.id, task_id, session)
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

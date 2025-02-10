from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.db import get_session
from tasks_backend.models.categories import Category
from tasks_backend.models.public import TaskPublicWithCategories
from tasks_backend.models.tasks import (
    Task,
    TaskCreate,
    TaskUpdate,
    get_task_or_raise_404,
)
from tasks_backend.models.users import User, get_user_or_raise_404
from tasks_backend.utils.auth_utils import get_current_user
from tasks_backend.utils.utils import get_current_utc_time

router = APIRouter(prefix="/tasks")


@router.post("/{user_id}", response_model=TaskPublicWithCategories)
def create_task(task_create: TaskCreate, user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    categories = session.exec(
        select(Category).where(Category.id.in_(task_create.category_ids))
    ).all()
    task = Task.model_validate(task_create, update={"categories": categories, "user_id": user_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{user_id}", response_model=list[TaskPublicWithCategories])
def read_tasks(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    print(f"current_user: {current_user}")
    get_user_or_raise_404(user_id, session)
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.get("/{user_id}/{task_id}", response_model=TaskPublicWithCategories)
def read_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    return task


@router.patch("/{user_id}/{task_id}", response_model=TaskPublicWithCategories)
def update_task(
    user_id: UUID, task_id: UUID, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    if task_update.category_ids:
        categories = session.exec(
            select(Category).where(Category.id.in_(task_update.category_ids))
        ).all()
        task.categories = categories
    task_update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_update_data)
    task.updated_at = get_current_utc_time()
    session.add(task)
    session.commit()
    session.refresh(task)
    print(task)
    return task


@router.delete("/{user_id}/{task_id}")
def delete_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.auth import get_current_user
from tasks_backend.db import get_session
from tasks_backend.models.categories import Category, CategoryCreate, CategoryUpdate, get_category_or_raise_404
from tasks_backend.models.public import CategoryPublicWithTasks
from tasks_backend.models.users import User

router = APIRouter(prefix="/categories")


@router.post("", response_model=CategoryPublicWithTasks)
def create_category(
    category_create: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    category = Category.model_validate(category_create, update={"user_id": current_user.id})
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("", response_model=list[CategoryPublicWithTasks])
def read_categories(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    categories = session.exec(select(Category).where(Category.user_id == current_user.id)).all()
    return categories


@router.get("/{category_id}", response_model=CategoryPublicWithTasks)
def read_category(
    category_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    category = get_category_or_raise_404(current_user.id, category_id, session)
    return category


@router.patch("/{category_id}", response_model=CategoryPublicWithTasks)
def update_category(
    category_id: UUID,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    category = get_category_or_raise_404(current_user.id, category_id, session)
    category_update_data = category_update.model_dump(exclude_unset=True)
    category.sqlmodel_update(category_update_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)
):
    category = get_category_or_raise_404(current_user.id, category_id, session)
    session.delete(category)
    session.commit()
    return {"message": "Category deleted", "category_id": category_id}

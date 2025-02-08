from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.db import get_session
from tasks_backend.models.categories import Category, CategoryCreate
from tasks_backend.models.users import get_user_or_raise_404

router = APIRouter(prefix="/categories")


@router.post("/{user_id}", response_model=Category)
def create_category(
    user_id: UUID, category_create: CategoryCreate, session: Session = Depends(get_session)
):
    get_user_or_raise_404(user_id, session)
    category = Category.model_validate(category_create, update={user_id: user_id})
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/{user_id}")
def read_categories(user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    categories = session.exec(select(Category)).all()
    return categories

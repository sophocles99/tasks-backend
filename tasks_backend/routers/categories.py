from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from tasks_backend.db import get_session
from tasks_backend.models.categories import Category, CategoryCreate, CategoryUpdate, get_category_or_raise_404
from tasks_backend.models.public import CategoryPublicWithTasks
from tasks_backend.models.users import get_user_or_raise_404

router = APIRouter(prefix="/categories")


@router.post("/{user_id}", response_model=CategoryPublicWithTasks)
def create_category(user_id: UUID, category_create: CategoryCreate, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    category = Category.model_validate(category_create, update={"user_id": user_id})
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/{user_id}", response_model=list[CategoryPublicWithTasks])
def read_categories(user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    categories = session.exec(select(Category)).all()
    return categories


@router.get("/{user_id}/{category_id}", response_model=CategoryPublicWithTasks)
def read_category(user_id: UUID, category_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    category = get_category_or_raise_404(user_id, category_id, session)
    return category


@router.patch("/{user_id}/{category_id}", response_model=CategoryPublicWithTasks)
def update_category(
    user_id: UUID,
    category_id: UUID,
    category_update: CategoryUpdate,
    session: Session = Depends(get_session),
):
    get_user_or_raise_404(user_id, session)
    category = get_category_or_raise_404(user_id, category_id, session)
    category_update_data = category_update.model_dump(exclude_unset=True)
    category.sqlmodel_update(category_update_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{user_id}/{category_id}")
def delete_category(user_id: UUID, category_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    category = get_category_or_raise_404(user_id, category_id, session)
    session.delete(category)
    session.commit()
    return {"message": "Category deleted", "category_id": category_id}

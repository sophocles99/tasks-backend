from enum import StrEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import Field, Relationship, Session, SQLModel, select

from tasks_backend.models.links import TaskCategoryLink

if TYPE_CHECKING:
    from tasks_backend.models.tasks import Task


class DefaultCategory(StrEnum):
    FINANCIAL = "financial"
    HEALTH = "health"
    HOME = "home"
    PERSONAL = "personal"
    WORK = "work"


DEFAULT_COLOURS: dict[DefaultCategory, int] = {
    DefaultCategory.FINANCIAL: 0x66BB6A,
    DefaultCategory.HEALTH: 0x03A9F4,
    DefaultCategory.HOME: 0xFF9800,
    DefaultCategory.PERSONAL: 0xFFEB3B,
    DefaultCategory.WORK: 0xEC05FF,
}


class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=20)
    colour: int = Field(ge=0, le=0xFFFFFF)


class Category(CategoryBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, unique=True)
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="categories", link_model=TaskCategoryLink)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: str | None = Field(default=None, min_length=3, max_length=20)
    colour: int | None = Field(default=None, ge=0, le=0xFFFFFF)


class CategoryPublic(CategoryBase):
    id: UUID


def create_default_categories(user_id: UUID, session: Session):
    default_categories = [
        Category(name=category.value, user_id=user_id, colour=DEFAULT_COLOURS[category]) for category in DefaultCategory
    ]
    session.add_all(default_categories)
    session.commit()


def restore_default_categories(user_id: UUID, session: Session):
    for category in DefaultCategory:
        existing_default_category = session.exec(select(Category).where(Category.name == category.value))
        if not existing_default_category:
            session.add(Category(name=category.value, user_id=user_id))
    session.commit()


def get_category_or_raise_404(user_id: UUID, category_id: UUID, session: Session):
    try:
        category = session.exec(select(Category).where(Category.id == category_id, Category.user_id == user_id)).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    except MultipleResultsFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="More than one category found")
    return category

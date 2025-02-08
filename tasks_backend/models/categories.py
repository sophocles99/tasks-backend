from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, Session, SQLModel, UniqueConstraint, select


class DefaultCategory(Enum):
    FINANCIAL = "financial"
    HEALTH = "health"
    HOME = "home"
    PERSONAL = "personal"
    WORK = "work"


class CategoryBase(SQLModel):
    name: str = Field(min_length=3, max_length=20)


class Category(CategoryBase, table=True):
    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_name_per_user_constraint"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")


class CategoryCreate(CategoryBase):
    pass


def create_default_categories(user_id: UUID, session: Session):
    default_categories = [
        Category(name=category.value, user_id=user_id) for category in DefaultCategory
    ]
    session.add_all(default_categories)
    session.commit()


def restore_default_categories(user_id: UUID, session: Session):
    for category in DefaultCategory:
        existing_default_category = session.exec(
            select(Category).where(Category.name == category.value)
        )
        if not existing_default_category:
            session.add(Category(name=category.value, user_id=user_id))
    session.commit()

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Field, Session, SQLModel

from tasks_backend.utils.utils import get_current_utc_time


class UserBase(SQLModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(unique=True)
    hashed_password: bytes = Field(max_length=60)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime | None = None
    last_login_at: datetime | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserPublic(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    last_login_at: datetime | None


class UserUpdate(SQLModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=50)


def get_user_or_raise_404(user_id: UUID, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

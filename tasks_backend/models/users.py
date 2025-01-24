from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from tasks_backend.utils.get_current_utc_time import get_current_utc_time


class UserBase(SQLModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=get_current_utc_time)
    updated_at: datetime = Field(default_factory=get_current_utc_time)
    last_login_at: datetime | None = None
    email: EmailStr = Field(unique=True)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None


class UserUpdate(SQLModel):
    first_name: str | None = Field(default=None, min_length=2, max_length=50)
    last_name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=50)

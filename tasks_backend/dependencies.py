from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from tasks_backend.auth import get_current_user
from tasks_backend.database.db import get_session
from tasks_backend.models.users import User

SessionDependency = Annotated[Session, Depends(get_session)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]

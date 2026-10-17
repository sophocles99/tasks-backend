from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from tasks_backend.auth import authenticate_user, create_access_token
from tasks_backend.dependencies import SessionDependency
from tasks_backend.models.auth import LoginResponse
from tasks_backend.utils.utils import get_current_utc_time

router = APIRouter(prefix="/auth")


@router.post("/login")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDependency
) -> LoginResponse:
    user = authenticate_user(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.last_login_at = get_current_utc_time()
    session.add(user)
    session.commit()
    session.refresh(user)
    access_token_response = create_access_token(user)
    return LoginResponse(
        access_token=access_token_response.access_token,
        email=user.email,
        first_name=user.first_name,
        id=user.id,
        last_name=user.last_name,
        token_type=access_token_response.token_type,
    )

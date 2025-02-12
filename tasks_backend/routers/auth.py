from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from tasks_backend.db import get_session
from tasks_backend.auth import (
    AccessTokenResponse,
    authenticate_user,
    create_access_token,
)

router = APIRouter(prefix="/auth")


@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> AccessTokenResponse:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_response = create_access_token(user)
    return access_token_response

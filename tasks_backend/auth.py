import os
from datetime import timedelta
from uuid import UUID

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlmodel import Session, select

from tasks_backend.db import get_session
from tasks_backend.models.users import User
from tasks_backend.utils.utils import get_current_utc_time

DEFAULT_ACCESS_TOKEN_EXPIRY_MINUTES = 30
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("Environment variable 'JWT_SECRET_KEY' is not set.")


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password)


def authenticate_user(email: str, password: str, session: Session):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(user: User) -> AccessTokenResponse:
    user_id: UUID = user.id
    user_id_jsonable = jsonable_encoder(user_id)
    current_utc_time = get_current_utc_time()
    expiry_time = current_utc_time + timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRY_MINUTES)
    access_token_payload = {"sub": user_id_jsonable, "exp": expiry_time}
    access_token = jwt.encode(access_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return AccessTokenResponse(access_token=access_token, token_type="bearer")


def get_current_user(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, [JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

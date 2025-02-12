from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from tasks_backend.auth import hash_password
from tasks_backend.db import get_session
from tasks_backend.models.categories import create_default_categories
from tasks_backend.models.users import User, UserCreate, UserPublic, UserUpdate, get_user_or_raise_404

router = APIRouter(prefix="/users")


@router.post("", response_model=UserPublic)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
    hashed_password = hash_password(user_create.password)
    user = User.model_validate(user_create, update={"hashed_password": hashed_password})
    session.add(user)
    session.commit()
    session.refresh(user)
    create_default_categories(user.id, session)
    return user


@router.get("", response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: UUID, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: UUID, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    user_update_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    session.delete(user)
    session.commit()
    return {"message": "User deleted", "user_id": user_id}

from contextlib import asynccontextmanager
from typing import Generator
from uuid import UUID
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from tasks_backend.db import create_tables, engine
from tasks_backend.models.tasks import Task, TaskCreate, TaskPublic, TaskUpdate
from tasks_backend.models.users import User, UserCreate, UserPublic, UserUpdate
from tasks_backend.utils.model_utils import get_task_or_raise_404, get_user_or_raise_404


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


app = FastAPI(lifespan=lifespan)


@app.post("/users", response_model=UserPublic)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
    hashed_password = bcrypt.hashpw(user_create.password.encode("utf-8"), bcrypt.gensalt())
    user = User.model_validate(user_create, update={"hashed_password": hashed_password})
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users", response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: UUID, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: UUID, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    user_update_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    user = get_user_or_raise_404(user_id, session)
    session.delete(user)
    session.commit()
    return {"message": "User deleted", "user_id": user_id}


@app.post("/tasks/{user_id}", response_model=TaskPublic)
def create_task(task_create: TaskCreate, user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = Task.model_validate(task_create, update={"user_id": user_id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{user_id}", response_model=list[TaskPublic])
def read_tasks(user_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@app.get("/tasks/{user_id}/{task_id}", response_model=TaskPublic)
def read_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    return task


@app.patch("/tasks/{user_id}/{task_id}", response_model=TaskPublic)
def update_task(
    user_id: UUID, task_id: UUID, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    task_update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{user_id}/{task_id}")
def delete_task(user_id: UUID, task_id: UUID, session: Session = Depends(get_session)):
    get_user_or_raise_404(user_id, session)
    task = get_task_or_raise_404(user_id, task_id, session)
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

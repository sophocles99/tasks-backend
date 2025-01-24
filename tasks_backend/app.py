from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from tasks_backend.db import create_tables, engine
from tasks_backend.models.tasks import Task, TaskCreate, TaskPublic, TaskUpdate
from tasks_backend.models.users import User, UserCreate, UserPublic, UserUpdate


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)


@app.post("/tasks", response_model=TaskPublic)
def create_task(task_create: TaskCreate, session: SessionDependency):
    new_task = Task.model_validate(task_create)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=list[TaskPublic])
def read_tasks(session: SessionDependency):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def read_task(task_id: int, session: SessionDependency):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDependency):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    task_update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDependency):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}


@app.post("/users", response_model=UserPublic)
def create_user(user_create: UserCreate, session: SessionDependency):
    new_user = User.model_validate(user_create)
    existing_user = session.exec(
        select(User).where(User.email == user_create.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already in use"
        )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[UserPublic])
def read_users(session: SessionDependency):
    users = session.exec(select(User)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user_update_data = user_update.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_update_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"message": "User deleted", "user_id": user_id}

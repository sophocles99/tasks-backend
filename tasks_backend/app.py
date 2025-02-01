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


@app.post("/users", response_model=UserPublic)
def create_user(user_create: UserCreate, session: SessionDependency):
    new_user = User(**user_create.model_dump())
    existing_user = session.exec(select(User).where(User.email == new_user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted", "user_id": user_id}


@app.post("/tasks/{user_id}", response_model=TaskPublic)
def create_task(task_create: TaskCreate, user_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404, detail="User not found")
    task = Task(**task_create.model_dump(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/{user_id}", response_model=list[TaskPublic])
def read_tasks(user_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404, detail="User not found")
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@app.get("/tasks/{user_id}/{task_id}", response_model=TaskPublic)
def read_task(user_id: int, task_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404, detail="User not found")
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).one()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@app.patch("/tasks/{user_id}/{task_id}", response_model=TaskPublic)
def update_task(user_id: int, task_id: int, task_update: TaskUpdate, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404, detail="User not found")
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).one()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(task_update_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{user_id}/{task_id}")
def delete_task(user_id: int, task_id: int, session: SessionDependency):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404, detail="User not found")
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).one()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

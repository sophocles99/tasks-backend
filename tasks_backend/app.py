from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from tasks_backend.db import create_tables, engine
from tasks_backend.models.tasks import Task, TaskCreate, TaskPublic, TaskUpdate


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
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDependency):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
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
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted", "task_id": task_id}

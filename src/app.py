from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import create_tables, engine
from models import Task, TaskCreate, TaskPublic


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/tasks", response_model=TaskPublic)
def create_task(task_create: TaskCreate):
    with Session(engine) as session:
        task = Task.model_validate(task_create)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/tasks", response_model=list[TaskPublic])
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def read_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, select

from database import create_tables, engine
from models import Task, TaskCreate


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/tasks")
def create_task(task_create: TaskCreate):
    with Session(engine) as session:
        task = Task.model_validate(task_create)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/tasks")
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks

from contextlib import asynccontextmanager

from fastapi import FastAPI

from tasks_backend.db import create_tables
from tasks_backend.routers import categories, tasks, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(categories.router)
app.include_router(tasks.router)
app.include_router(users.router)

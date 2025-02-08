from contextlib import asynccontextmanager

from fastapi import FastAPI

from tasks_backend.db import create_tables
from tasks_backend.routers import categories_router, tasks_router, users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(categories_router.router)
app.include_router(tasks_router.router)
app.include_router(users_router.router)

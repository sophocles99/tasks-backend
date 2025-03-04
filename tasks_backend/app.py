from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from mangum import Mangum

from tasks_backend.db import create_tables
from tasks_backend.routers import auth, categories, tasks, users


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root(request: Request):
    print(request.scope.get("aws.event", {}))
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(tasks.router)
app.include_router(users.router)

lambda_handler = Mangum(app)

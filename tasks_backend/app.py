import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from tasks_backend.db import create_tables
from tasks_backend.routers import auth, categories, tasks, users

_invocation_count = 0


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan, root_path="/Prod")

origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(request: Request):
    logging.info("Running root operation function")
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        message = (
            f"FastAPI running on AWS Lambda in region {os.getenv('AWS_REGION')}, "
            f"using runtime environment {os.getenv('AWS_EXECUTION_ENV')}"
        )
    else:
        message = "FastAPI running locally"
    return {"message": message}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(tasks.router)
app.include_router(users.router)


def lambda_handler(event, context):
    global _invocation_count
    _invocation_count += 1
    logging.info(f"Invocation count: {_invocation_count}")
    logging.info(event)
    asgi_handler = Mangum(app, lifespan="auto")
    response = asgi_handler(event, context)

    return response

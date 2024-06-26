from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.student_router import student_router
from server.routes.task_router import task_router

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router, tags=["students"], prefix="/students")
app.include_router(task_router, tags=["tasks"], prefix="/tasks")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the task app"}

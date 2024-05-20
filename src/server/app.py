from fastapi import FastAPI
from server.routes.student_router import student_router

app = FastAPI()
app.include_router(student_router, tags=["students"], prefix="/students")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the todo app"}

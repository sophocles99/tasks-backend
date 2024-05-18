from fastapi import FastAPI
from server.routes.student_router import router as StudentRouter

app = FastAPI()
app.include_router(StudentRouter, tags=["students"], prefix="/students")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the todo app"}

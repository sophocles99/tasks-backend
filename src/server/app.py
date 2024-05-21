from fastapi import FastAPI
from server.routes.student_router import student_router
from server.routes.todo_router import todo_router


app = FastAPI()
app.include_router(student_router, tags=["students"], prefix="/students")
app.include_router(todo_router, tags=["todos"], prefix="/todos")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the todo app"}

from fastapi import APIRouter, HTTPException
from server.models.todo_models import (
    create_todo,
    remove_todo,
    retrieve_todo,
    retrieve_todos,
    update_todo,
)
from server.schemas.todo_schemas import Todo, TodoUpdate

todo_router = APIRouter()


@todo_router.get("/", response_description="Todos retrieved from database")
async def get_todos() -> list[Todo]:
    todos = await retrieve_todos()
    return todos


@todo_router.get("/{id}", response_description="Todo retrieved from database")
async def get_todo(id: str) -> Todo:
    todo = await retrieve_todo(id)
    if not todo:
        raise HTTPException(status_code=404, detail="No todo found with that id")
    return todo


@todo_router.post("/", response_description="Todo added into database", status_code=201)
async def post_todo(todo: Todo) -> Todo:
    todo_dict = todo.model_dump()
    new_todo = await create_todo(todo_dict)
    return new_todo


@todo_router.patch("/{id}", response_description="Todo updated")
async def patch_todo(id: str, todo_update: TodoUpdate) -> Todo:
    todo_update_dict = {k: v for k, v in todo_update if v is not None}
    updated_todo = await update_todo(id, todo_update_dict)
    return updated_todo


@todo_router.delete("/{id}", response_description="Todo deleted", status_code=204)
async def delete_todo(id: str) -> None:
    delete_success = await remove_todo(id)
    if not delete_success:
        raise HTTPException(status_code=404, detail="No todo found with that id")
    return None

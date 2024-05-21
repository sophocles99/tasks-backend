from bson import ObjectId
from server.schemas.todo_schemas import Todo
from server.database import todo_collection


# create student
async def create_todo(todo: Todo) -> Todo | None:
    insert_one_result = await todo_collection.insert_one(todo)
    new_todo = await todo_collection.find_one(insert_one_result.inserted_id)
    return new_todo


# retrieve all students
async def retrieve_todos() -> list[Todo]:
    todos = [todo async for todo in todo_collection.find()]
    return todos


# retrieve student by id
async def retrieve_todo(id: str) -> Todo | None:
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        return todo
    return None


# update a student by id
async def update_todo(id: str, todo_update: dict) -> Todo | None:
    updated_todo = await todo_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": todo_update}, return_document=True
    )
    return updated_todo


# delete a student by id
async def remove_todo(id: str) -> Todo | None:
    todo = todo_collection.find_one_and_delete({"_id": ObjectId(id)})
    if todo:
        return True
    return False

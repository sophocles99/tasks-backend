from bson import ObjectId
from datetime import datetime
from server.database import todo_collection


# create student
async def create_todo(todo: dict) -> dict | None:
    todo["created_at"] = datetime.now()
    insert_todo_result = await todo_collection.insert_one(todo)
    new_todo = await todo_collection.find_one(insert_todo_result.inserted_id)
    return new_todo


# retrieve all students
async def retrieve_todos() -> list[dict]:
    todos = [todo async for todo in todo_collection.find()]
    return todos


# retrieve student by id
async def retrieve_todo(id: str) -> dict | None:
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo:
        return todo
    return None


# update a student by id
async def update_todo(id: str, todo_update) -> dict | None:
    updated_todo = await todo_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": todo_update}, return_document=True
    )
    return updated_todo


# delete a student by id
async def remove_todo(id: str) -> bool:
    todo = todo_collection.find_one_and_delete({"_id": ObjectId(id)})
    if todo:
        return True
    return False

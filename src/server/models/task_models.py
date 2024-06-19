from datetime import datetime

from bson import ObjectId
from server.database import task_collection


# create student
async def create_task(task: dict) -> dict | None:
    task["status"] = "not done"
    task["created_at"] = datetime.now()
    insert_task_result = await task_collection.insert_one(task)
    new_task = await task_collection.find_one(insert_task_result.inserted_id)
    return new_task


# retrieve all students
async def retrieve_tasks() -> list[dict]:
    tasks = [task async for task in task_collection.find()]
    return tasks


# retrieve student by id
async def retrieve_task(id: str) -> dict | None:
    task = await task_collection.find_one({"_id": ObjectId(id)})
    if task:
        return task
    return None


# update a student by id
async def update_task(id: str, task_update) -> dict | None:
    updated_task = await task_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": task_update}, return_document=True
    )
    return updated_task


# delete a student by id
async def remove_task(id: str) -> bool:
    task = task_collection.find_one_and_delete({"_id": ObjectId(id)})
    if task:
        return True
    return False

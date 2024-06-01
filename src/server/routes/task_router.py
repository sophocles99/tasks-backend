from fastapi import APIRouter, HTTPException
from server.models.task_models import (
    create_task,
    remove_task,
    retrieve_task,
    retrieve_tasks,
    update_task,
)
from server.schemas.task_schemas import ObjectIdStr, TaskIn, TaskOut, TaskUpdate

task_router = APIRouter()


@task_router.get(
    "/",
    response_description="Tasks retrieved from database",
    response_model_by_alias=False,
)
async def get_tasks() -> list[TaskOut]:
    tasks = await retrieve_tasks()
    return tasks


@task_router.get(
    "/{id}",
    response_description="Task retrieved from database",
    response_model_by_alias=False,
)
async def get_task(id: ObjectIdStr) -> TaskOut:
    task = await retrieve_task(id)
    if not task:
        raise HTTPException(status_code=404, detail="No task found with that id")
    return task


@task_router.post(
    "/",
    response_description="Task added into database",
    response_model_by_alias=False,
    status_code=201,
)
async def post_task(task: TaskIn) -> TaskOut:
    task_dict = task.model_dump()
    new_task = await create_task(task_dict)
    return new_task


@task_router.patch(
    "/{id}", response_description="Task updated", response_model_by_alias=False
)
async def patch_task(id: str, task_update: TaskUpdate) -> TaskOut:
    task_update_dict = {k: v for k, v in task_update if v is not None}
    updated_task = await update_task(id, task_update_dict)
    return updated_task


@task_router.delete("/{id}", response_description="Task deleted", status_code=204)
async def delete_task(id: str) -> None:
    delete_success = await remove_task(id)
    if not delete_success:
        raise HTTPException(status_code=404, detail="No task found with that id")
    return None

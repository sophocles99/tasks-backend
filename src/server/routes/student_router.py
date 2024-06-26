from fastapi import APIRouter, HTTPException
from server.models.student_models import (
    create_student,
    remove_student,
    retrieve_student,
    retrieve_students,
    update_student,
)
from server.schemas.student_schemas import Student, StudentUpdate, StudentWithId

student_router = APIRouter()


@student_router.get("/", response_description="Students retrieved from database")
async def get_students() -> list[StudentWithId]:
    students = await retrieve_students()
    return students


@student_router.get("/{id}", response_description="Student retrieved from database")
async def get_student(id: str) -> StudentWithId:
    student = await retrieve_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="No student found with that id")
    return student


@student_router.post("/", response_description="Student added into database", status_code=201)
async def post_student(student: Student) -> StudentWithId:
    student_dict = student.model_dump()
    new_student = await create_student(student_dict)
    return new_student


@student_router.patch("/{id}", response_description="Student updated")
async def patch_student(id: str, student_update: StudentUpdate) -> StudentWithId:
    update_dict = {k: v for k, v in student_update if v is not None}
    updated_student = await update_student(id, update_dict)
    return updated_student


@student_router.delete("/{id}", response_description="Student deleted", status_code=204)
async def delete_student(id: str) -> None:
    delete_success = await remove_student(id)
    if not delete_success:
        raise HTTPException(status_code=404, detail="No student found with that id")
    return None

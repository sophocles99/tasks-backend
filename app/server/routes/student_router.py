from fastapi import APIRouter, HTTPException

from server.database import (
    retrieve_students,
    retrieve_student,
    create_student,
    update_student,
    delete_student,
)

from server.models.student_model import Student, StudentUpdate  # CreateErrorResponse,

router = APIRouter()


@router.get("/", response_description="Students retrieved from database")
async def get_students():
    students = await retrieve_students()
    return students


@router.get("/{id}", response_description="Student retrieved from database")
async def get_student(id: str):
    student = await retrieve_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="No student found with that id")
    return student


@router.post("/", response_description="Student added into database")
async def post_student(student: Student):
    student_dict = student.model_dump()
    new_student = await create_student(student_dict)
    return new_student


@router.patch("/{id}", response_description="Student updated")
async def patch_student(id: str, student_update: StudentUpdate):
    update_dict = {k: v for k, v in student_update if v is not None}
    updated_student = await update_student(id, update_dict)
    return updated_student

from fastapi import APIRouter

from server.database import (  # delete_student,; retrieve_student,; retrieve_students,; update_student,
    create_student,
)

from server.models.student_model import (
    # CreateErrorResponse,
    CreateResponse,
    Student,
    # UpdateStudent,
)

router = APIRouter()


@router.post("/", response_description="Student added into the database")
async def post_student(student: Student):
    student_dict = student.model_dump()
    new_student = await create_student(student_dict)
    return CreateResponse(new_student, "Student added successfully.")

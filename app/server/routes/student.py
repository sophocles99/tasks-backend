from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    create_student,
    # delete_student,
    # retrieve_student,
    # retrieve_students,
    # update_student,
)
from server.models.student import (
    # ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    # UpdateStudentModel,
)

router = APIRouter()


@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await create_student(student)
    return ResponseModel(new_student, "Student added successfully.")

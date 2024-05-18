from pydantic import BaseModel, EmailStr, Field


class Student(BaseModel):
    fullname: str
    email: EmailStr
    course_of_study: str
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., gt=0.0, le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
            }
        }


class UpdateStudent(BaseModel):
    fullname: str | None
    email: EmailStr | None
    course_of_study: str | None
    year: int | None
    gpa: float | None

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
            }
        }


def CreateResponse(data, message):
    return {"data": [data], "code": 200, "message": message}


def CreateErrorResponse(error, code, message):
    return {"error": error, "code": code, "message": message}

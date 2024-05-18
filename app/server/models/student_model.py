from pydantic import BaseModel, EmailStr, Field, model_validator


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


class StudentUpdate(BaseModel):
    fullname: str | None = None
    email: EmailStr | None = None
    course_of_study: str | None = None
    year: int | None = None
    gpa: float | None = None

    @model_validator(mode="before")
    def at_least_one_field(cls, data):
        data_fields = data.keys()
        model_fields = cls.model_fields.keys()
        if not any(map(lambda field: field in model_fields, data_fields)):
            raise ValueError(
                f"at least one of the following fields is required: {", ".join(list(model_fields))}"
            )
        return data

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources and environmental engineering",
                "year": 4,
                "gpa": "4.0",
            }
        }


def CreateErrorResponse(error, code, message):
    return {"error": error, "code": code, "message": message}

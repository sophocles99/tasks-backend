from pydantic import BaseModel, EmailStr, Field, model_validator


class Student(BaseModel):
    fullname: str
    email: EmailStr
    course_of_study: str
    year: int = Field(..., gt=0, lt=9)
    gpa: float = Field(..., gt=0.0, le=4.0)

    class Config:
        json_schema_extra = {
            "example": {
                "course_of_study": "Water resources engineering",
                "email": "jdoe@x.edu.ng",
                "fullname": "John Doe",
                "gpa": "3.0",
                "year": 2,
            }
        }


class StudentWithId(Student):
    id: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "664a1956ba41751e455e7042",
                "course_of_study": "Water resources engineering",
                "email": "jdoe@x.edu.ng",
                "fullname": "John Doe",
                "gpa": "3.0",
                "year": 2,
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
        json_schema_extra = {
            "example": {
                "course_of_study": "Water resources and environmental engineering",
                "year": 3,
            }
        }


def CreateErrorResponse(error, code, message):
    return {"error": error, "code": code, "message": message}

from datetime import datetime
from typing import Annotated, Literal

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field, model_validator


def validate_object_id(value: str | ObjectId) -> str:
    assert ObjectId.is_valid(value), f"{value} is not a valid ObjectId"
    return value.__str__()


ObjectIdStr = Annotated[str, BeforeValidator(validate_object_id)]


class TaskIn(BaseModel):
    title: str
    description: str
    status: Literal["done", "not done", "in progress"] = "not done"


class TaskOut(TaskIn):
    created_at: datetime
    id: ObjectIdStr = Field(alias="_id")


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["done", "not done", "in progress"] | None = None

    @model_validator(mode="before")
    def at_least_one_field(cls, data):
        data_fields = data.keys()
        model_fields = cls.model_fields.keys()
        if not any(map(lambda field: field in model_fields, data_fields)):
            raise ValueError(
                f"at least one of the following fields is required: {", ".join(list(model_fields))}"
            )
        return data

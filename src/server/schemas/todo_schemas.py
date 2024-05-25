from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, BeforeValidator, Field
from typing import Annotated, Literal


def validate_object_id(value: str | ObjectId) -> str:
    assert ObjectId.is_valid(value), f"{value} is not a valid ObjectId"
    return value.__str__()


ObjectIdStr = Annotated[str, BeforeValidator(validate_object_id)]


class TodoIn(BaseModel):
    title: str
    description: str
    status: Literal["done", "not done", "in progress"] = "not done"


class TodoOut(TodoIn):
    created_at: datetime
    id: ObjectIdStr = Field(alias="_id")


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Literal["done", "not done", "in progress"] | None = None

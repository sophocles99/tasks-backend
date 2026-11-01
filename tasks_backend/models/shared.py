from sqlmodel import SQLModel

from tasks_backend.models.categories import CategoryPublic
from tasks_backend.models.tasks import TaskPublic


# Inherit from SQLModel to allow UserCreateResponse to inherit from both UserBase and AccessTokenResponse
class AccessTokenResponse(SQLModel):
    access_token: str
    token_type: str


class CategoryPublicWithTasks(CategoryPublic):
    tasks: list["TaskPublic"]

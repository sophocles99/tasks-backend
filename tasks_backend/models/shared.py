from pydantic import BaseModel

from tasks_backend.models.categories import CategoryPublic
from tasks_backend.models.tasks import TaskPublic


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class CategoryPublicWithTasks(CategoryPublic):
    tasks: list["TaskPublic"]


class TaskPublicWithCategories(TaskPublic):
    categories: list["CategoryPublic"]

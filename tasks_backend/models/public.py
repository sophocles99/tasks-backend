from tasks_backend.models.categories import CategoryPublic
from tasks_backend.models.tasks import TaskPublic


class CategoryPublicWithTasks(CategoryPublic):
    tasks: list["TaskPublic"]


class TaskPublicWithCategories(TaskPublic):
    categories: list["CategoryPublic"]

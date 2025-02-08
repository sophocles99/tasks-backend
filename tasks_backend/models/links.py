from uuid import UUID

from sqlmodel import Field, SQLModel


class TaskCategoryLink(SQLModel, table=True):
    task_id: UUID = Field(foreign_key="task.id", primary_key=True)
    category_id: UUID = Field(foreign_key="category.id", primary_key=True)

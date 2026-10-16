import json
import logging
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from sqlmodel import Session, select

from tasks_backend.auth import hash_password
from tasks_backend.database.db import get_engine
from tasks_backend.models.categories import Category, create_default_categories
from tasks_backend.models.tasks import Task, TaskBase
from tasks_backend.models.users import User, UserCreate

SEED_DATA_FILEPATH = Path(__file__).parent / "seed-data.json"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeedTask(TaskBase):
    model_config = ConfigDict(extra="forbid")

    category: str | None = None


class SeedData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user: UserCreate
    tasks: list[SeedTask]


def load_seed_data() -> SeedData:
    with open(SEED_DATA_FILEPATH, "r") as f:
        seed_data = json.load(f)
    return SeedData.model_validate(seed_data)


def seed_database():
    seed_data = load_seed_data()

    user_create = seed_data.user
    logger.info(f"New user: {user_create}")
    engine = get_engine()

    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            logger.warning(f"User with email address {user_create.email} already exists. Ending seeding process.")
            return

        hashed_password = hash_password(user_create.password)
        user = User.model_validate(user_create, update={"hashed_password": hashed_password})
        session.add(user)
        session.commit()
        session.refresh(user)

        create_default_categories(user.id, session)
        user_categories = session.exec(select(Category).where(Category.user_id == user.id)).all()
        user_category_ids_by_name = {category.name: category.id for category in user_categories}

        tasks: list[Task] = []
        for seed_task in seed_data.tasks:
            category_id = user_category_ids_by_name.get(seed_task.category)
            task = Task.model_validate(
                seed_task.model_dump(exclude={"category"}),
                update={"user_id": user.id, "category_id": category_id},
            )
            tasks.append(task)

        session.add_all(tasks)
        session.commit()


if __name__ == "__main__":
    seed_database()

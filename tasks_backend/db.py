import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DB_URL = os.getenv("DB_URL", None)
if not DB_URL:
    raise ValueError("Environment variable 'DB_URL' is not set.")

engine = create_engine(DB_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_tables():
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

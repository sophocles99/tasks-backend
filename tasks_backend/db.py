import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

db_url = os.getenv("DB_URL", None)
print(f"db_url: {db_url}")
if not db_url:
    raise ValueError("Environment variable 'DB_URL' is not set.")

engine = create_engine(db_url, echo=True)


def create_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

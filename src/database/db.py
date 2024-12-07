import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel

load_dotenv()

db_url = os.getenv("DB_URL", None)
if not db_url:
    raise ValueError("Environment variable 'DB_URL' is not set.")

engine = create_engine(db_url, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

import logging
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from tasks_backend.utils.get_db_url import get_db_url

logging.basicConfig(level=logging.INFO)
load_dotenv()

db_url = get_db_url()
engine = create_engine(db_url, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_tables():
    # SQLModel.metadata.drop_all(engine)
    tables_list = ", ".join(table_name for table_name in SQLModel.metadata.tables)
    logging.info(f"Creating tables {tables_list} from SQLModel metadata")
    SQLModel.metadata.create_all(engine)

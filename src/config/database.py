from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

from sqlmodel import SQLModel, create_engine


DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)

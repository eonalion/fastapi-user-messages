from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine


DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    SQLModel.metadata.create_all(engine)

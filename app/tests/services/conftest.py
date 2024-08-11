import pytest
from sqlmodel import SQLModel, create_engine, Session, StaticPool


@pytest.fixture
def session():
    # Configure the in-memory SQLite database
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

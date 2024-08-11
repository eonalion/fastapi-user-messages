from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

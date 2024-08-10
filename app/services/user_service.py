import uuid
from typing import Optional

from sqlmodel import Session, select

from app.models.user import UserCreate, User


def create_user(session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    user = select(User).where(User.email == email)
    result_user = session.exec(user).first()
    return result_user


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    user = session.get(User, user_id)
    return user

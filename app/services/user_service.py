import uuid
from typing import Optional

from sqlmodel import Session, select

from app.services.exceptions import NotFoundError, AlreadyExistsError
from app.models.user import UserCreate, User, UserUpdate
import app.core.resources as res


def get_users(session: Session, limit: int) -> list[User]:
    results = session.exec(select(User).limit(limit)).all()
    return results


def get_user_by_email(session: Session, email: str) -> User:
    user = _get_user_by_email(session=session, email=email)
    if not user:
        raise NotFoundError(message=res.USER_NOT_FOUND)
    return user


def _get_user_by_email(session: Session, email: str) -> Optional[User]:
    user = select(User).where(User.email == email)
    result_user = session.exec(user).first()
    return result_user


def get_user_by_id(session: Session, user_id: uuid.UUID) -> User:
    user = session.get(User, user_id)
    if not user:
        raise NotFoundError(message=res.USER_NOT_FOUND)
    return user


def create_user(session: Session, user_in: UserCreate) -> User:
    user = _get_user_by_email(session=session, email=user_in.email)
    if user:
        raise AlreadyExistsError(message=res.EMAIL_ALREADY_EXISTS)
    user = User.model_validate(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
    user = get_user_by_id(session=session, user_id=user_id)
    if user_in.email:
        user_by_email = _get_user_by_email(session=session, email=user_in.email)
        if user_by_email and user_by_email.id != user_id:
            raise AlreadyExistsError(message=res.EMAIL_ALREADY_EXISTS)

    user_update_data: dict = user_in.model_dump(exclude_unset=True)
    if user_update_data:
        user.sqlmodel_update(user_update_data)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def delete_user(session: Session, user_id: uuid.UUID) -> None:
    user = get_user_by_id(session=session, user_id=user_id)
    session.delete(user)
    session.commit()

import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.api.dependencies import SessionDep
from app.models.user import UserPublic, UserCreate, UserUpdate, User
from app.services import user_service
from app.models.util import Message

router = APIRouter()


@router.get("/", response_model=list[UserPublic])
def get_users(session: SessionDep):
    users: list[User] = user_service.get_users(session=session)
    return users


@router.get("/{email}", response_model=UserPublic)
def get_user_by_email(email: str, session: SessionDep):
    user: Optional[User] = user_service.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    return user


@router.post("/", response_model=UserPublic)
def create_user(user_in: UserCreate, session: SessionDep):
    user: Optional[User] = user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists.",
        )

    user_created: User = user_service.create_user(session=session, user_create=user_in)
    return user_created


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate):
    user: Optional[User] = user_service.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    if user_in.email:
        user_by_email: Optional[User] = user_service.get_user_by_email(session=session, email=user_in.email)
        if user_by_email and user_by_email.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists.",
            )

    user_updated: User = user_service.update_user(session=session, user=user, user_update=user_in)
    return user_updated


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    user: Optional[User] = user_service.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )
    user_service.delete_user(session=session, user=user)
    return Message(message="User deleted successfully.")

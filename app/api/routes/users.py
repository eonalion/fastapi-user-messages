import uuid

from fastapi import APIRouter, Query

from app.api.dependencies import SessionDep
from app.core.constants import DEFAULT_USER_LIMIT, MAXIMUM_USER_LIMIT
from app.models.user import UserPublic, UserCreate, UserUpdate, User
from app.services import user_service
from app.models.util import ResponseMessage
from pydantic import EmailStr

router = APIRouter()


@router.get("/", response_model=list[UserPublic])
def get_users(
    session: SessionDep,
    limit: int = Query(default=DEFAULT_USER_LIMIT, le=MAXIMUM_USER_LIMIT),
):
    users: list[User] = user_service.get_users(session=session, limit=limit)
    return users


@router.get("/{email}", response_model=UserPublic)
def get_user_by_email(email: EmailStr, session: SessionDep):
    user = user_service.get_user_by_email(session=session, email=email)
    return user


@router.post("/", response_model=UserPublic)
def create_user(user_in: UserCreate, session: SessionDep):
    user_created: User = user_service.create_user(session=session, user_in=user_in)
    return user_created


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate):
    user_updated: User = user_service.update_user(
        session=session, user_id=user_id, user_in=user_in
    )
    return user_updated


@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    user_service.delete_user(session=session, user_id=user_id)
    return ResponseMessage(message="User deleted successfully.")

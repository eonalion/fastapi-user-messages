import uuid

from fastapi import APIRouter, HTTPException

from app.api.dependencies import SessionDep
from app.models.user import UserPublic, UserCreate, UserUpdate
from app.services import user_service

router = APIRouter()


@router.get("/{email}", response_model=UserPublic)
def get_user_by_email(email: str, session: SessionDep):
    user = user_service.get_user_by_email(session=session, email=email)
    return user


@router.post("/", response_model=UserPublic)
def create_user(user_in: UserCreate, session: SessionDep):
    user = user_service.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user_created = user_service.create_user(session=session, user_create=user_in)
    return user_created


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: uuid.UUID, user_in: UserUpdate, session: SessionDep):
    pass


@router.patch("/{user_id}")
def delete_user(user_id: uuid.UUID, session: SessionDep):
    return "User deleted successfully."

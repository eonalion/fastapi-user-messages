import uuid
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


# Shared models
class UserBase(SQLModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)


# API models CRUD
class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = Field(default=None, max_length=255)


class UserPublic(UserBase):
    id: uuid.UUID


# Database models
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    messages: list["Message"] = Relationship(  # noqa: F821
        back_populates="sender", cascade_delete=True
    )

# Shared properties
import uuid
from sqlmodel import SQLModel, Field, Relationship

from app.models.user import User


# Shared models
class MessageBase(SQLModel):
    sender_id: uuid.UUID
    content: str = Field(max_length=1000)
    timestamp: str = Field(max_length=1000)


# API models CRUD
class MessageCreate(MessageBase):
    pass


class MessagePublic(MessageBase):
    id: uuid.UUID


# Database models
class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sender_id = Field(foreign_key="user.id")
    sender: "User" = Relationship(back_populates="messages")

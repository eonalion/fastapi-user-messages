# Shared properties
import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


# Shared models
class MessageBase(SQLModel):
    content: str = Field(max_length=1000)


# API models CRUD
class MessageCreate(MessageBase):
    pass


class MessagePublic(MessageBase):
    id: uuid.UUID
    timestamp: datetime


# Database models
class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    sender_id: uuid.UUID = Field(foreign_key="user.id")
    sender: "User" = Relationship(back_populates="messages")

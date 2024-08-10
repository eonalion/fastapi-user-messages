from uuid import UUID

from sqlmodel import Session, select

from app.models import Message, User
from app.models.message import MessageCreate
from app.services import user_service


def get_user_messages(session: Session, user_id: UUID) -> list[Message]:
    query = select(Message).where(Message.sender_id == user_id)
    results = session.exec(query)
    return results.all()


def create_message(session: Session, user_id: UUID, message_in: MessageCreate) -> Message:
    user = user_service.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise ValueError("User not found.")
    message = Message(**message_in.dict(), sender_id=user_id)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

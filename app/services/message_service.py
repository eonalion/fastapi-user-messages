from uuid import UUID

from sqlmodel import Session, select

from app.core.exceptions import NotFoundError
from app.models import Message
from app.models.message import MessageCreate
from app.services import user_service
import app.core.resources as res


def get_user_messages(session: Session, user_id: UUID) -> list[Message]:
    user = user_service.get_user_by_id(session=session, user_id=user_id)
    query = select(Message).where(Message.sender_id == user.id)
    results = session.exec(query)
    return results.all()


def get_message_for_user(session: Session, user_id: UUID, message_id: UUID) -> Message:
    user = user_service.get_user_by_id(session=session, user_id=user_id)
    query = select(Message).where(Message.sender_id == user.id).where(Message.id == message_id)
    message = session.exec(query).first()
    if not message:
        raise NotFoundError(message=res.MESSAGE_NOT_FOUND)
    return message


def create_message_for_user(session: Session, user_id: UUID, message_in: MessageCreate) -> Message:
    user = user_service.get_user_by_id(session=session, user_id=user_id)
    message = Message(**message_in.dict(), sender_id=user.id)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def delete_message_for_user(session: Session, user_id: UUID, message_id: UUID) -> None:
    message = get_message_for_user(session=session, user_id=user_id, message_id=message_id)
    session.delete(message)
    session.commit()

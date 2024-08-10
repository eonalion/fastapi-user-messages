from uuid import UUID

from fastapi import APIRouter

from app.api.dependencies import SessionDep
from app.models.message import MessagePublic, MessageCreate
from app.models.util import ResponseMessage
from app.services import message_service

router = APIRouter()


@router.get("/", response_model=list[MessagePublic])
def list_user_messages(user_id: UUID, session: SessionDep):
    messages = message_service.get_user_messages(session=session, user_id=user_id)
    return messages


@router.post("/", response_model=MessagePublic)
def create_message_for_user(user_id: UUID, message_in: MessageCreate, session: SessionDep):
    message = message_service.create_message_for_user(session=session, user_id=user_id, message_in=message_in)
    return message


@router.delete("/{message_id}", response_model=ResponseMessage)
def delete_message_for_user(user_id: UUID, message_id: UUID, session: SessionDep):
    message_service.delete_message_for_user(session=session, user_id=user_id, message_id=message_id)
    return ResponseMessage(message="Message deleted successfully.")

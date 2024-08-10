from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.dependencies import SessionDep
from app.models.message import MessagePublic, MessageCreate
from app.services.message_service import get_user_messages, create_message

router = APIRouter()


@router.get("/", response_model=list[MessagePublic])
def list_user_messages(user_id: UUID, session: SessionDep):
    messages = get_user_messages(session=session, user_id=user_id)
    return messages


@router.post("/", response_model=MessagePublic)
def create_message_for_user(user_id: UUID, message_in: MessageCreate, session: SessionDep):
    try:
        message = create_message(session=session, user_id=user_id, message_in=message_in)
        return message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


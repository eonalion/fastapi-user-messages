from app.services.exceptions import NotFoundError
from app.models.message import MessageCreate
from app.models.user import UserCreate
from app.services.message_service import (
    create_message_for_user,
    get_user_messages,
    get_message_for_user,
    delete_message_for_user,
)
from app.services.user_service import create_user
from app.tests.utils import generate_random_email, generate_random_name, generate_uuid
import pytest
import app.core.resources as res


def test_create_message_for_user__message_created__message_returned(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    message_content = "Test message"
    message = create_message_for_user(
        session=session,
        user_id=user.id,
        message_in=MessageCreate(content=message_content),
    )

    assert message.content == message_content
    assert message.sender_id == user.id
    assert message.sender == user
    assert message.id is not None
    assert message.timestamp is not None


def test_create_message_for_user__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        create_message_for_user(
            session=session,
            user_id=user_id,
            message_in=MessageCreate(content="Test message"),
        )

    assert err.value.message == res.USER_NOT_FOUND


def test_get_user_messages__no_messages_found__empty_list_returned(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )

    result_messages = get_user_messages(session=session, user_id=user.id)

    assert result_messages == []


def test_get_user_messages__messages_found__messages_returned(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    messages = [
        create_message_for_user(
            session=session,
            user_id=user.id,
            message_in=MessageCreate(content=f"Test Message {i}"),
        )
        for i in range(3)
    ]

    result_messages = get_user_messages(session=session, user_id=user.id)

    assert len(result_messages) == 3
    for message in messages:
        assert message in result_messages


def test_get_message_for_user__message_found__message_returned(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    message_content = "Test message"
    message = create_message_for_user(
        session=session,
        user_id=user.id,
        message_in=MessageCreate(content=message_content),
    )

    result_message = get_message_for_user(
        session=session, user_id=user.id, message_id=message.id
    )

    assert result_message.content == message_content
    assert result_message.sender_id == user.id
    assert result_message.sender == user
    assert result_message.id == message.id
    assert result_message.timestamp == message.timestamp


def test_get_message_for_user__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()
    message_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        get_message_for_user(session=session, user_id=user_id, message_id=message_id)

    assert err.value.message == res.USER_NOT_FOUND


def test_get_message_for_user__message_not_found__not_found_error_raised(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    message_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        get_message_for_user(session=session, user_id=user.id, message_id=message_id)

    assert err.value.message == res.MESSAGE_NOT_FOUND


def test_delete_message_for_user__message_deleted__no_return(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    message = create_message_for_user(
        session=session,
        user_id=user.id,
        message_in=MessageCreate(content="Test message"),
    )

    delete_message_for_user(session=session, user_id=user.id, message_id=message.id)

    with pytest.raises(NotFoundError) as err:
        get_message_for_user(session=session, user_id=user.id, message_id=message.id)

    assert err.value.message == res.MESSAGE_NOT_FOUND


def test_delete_message_for_user__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()
    message_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        delete_message_for_user(session=session, user_id=user_id, message_id=message_id)

    assert err.value.message == res.USER_NOT_FOUND


def test_delete_message_for_user__message_not_found__not_found_error_raised(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    message_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        delete_message_for_user(session=session, user_id=user.id, message_id=message_id)

    assert err.value.message == res.MESSAGE_NOT_FOUND

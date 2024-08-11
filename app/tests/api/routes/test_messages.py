from uuid import UUID

import app.core.resources as res

from app.core.exceptions import NotFoundError
from app.models import Message
from app.models.message import MessageCreate

USER_ID = "b6f37031-672d-4770-b6e8-ca34fad01968"
MESSAGES_ROUTE_PATH = f"/users/{USER_ID}/messages"


def test_get_user_messages__messages_found__messages_returned(
    mocker, test_client, mock_session
):
    expected_messages = [
        {
            "id": "131637b2-dc9a-4907-87b6-5c65eb9e9013",
            "sender_id": USER_ID,
            "content": "Message 1",
            "timestamp": "2021-08-01T00:00:00Z",
        },
        {
            "id": "55fab7d8-a109-433c-b2f9-98a5b89ddcef",
            "sender_id": USER_ID,
            "content": "Message 2",
            "timestamp": "2021-08-02T00:00:00Z",
        },
    ]
    mock_messaged = [Message(**expected_messages[0]), Message(**expected_messages[1])]
    mocked_get_user_messages = mocker.patch(
        "app.api.routes.messages.message_service.get_user_messages",
        return_value=mock_messaged,
    )

    response = test_client.get(f"{MESSAGES_ROUTE_PATH}/")

    mocked_get_user_messages.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID)
    )
    assert response.status_code == 200
    assert response.json() == expected_messages


def test_get_user_messages__messages_not_found__empty_list_returned(
    mocker, test_client, mock_session
):
    mock_messaged = []
    mocked_get_user_messages = mocker.patch(
        "app.api.routes.messages.message_service.get_user_messages",
        return_value=mock_messaged,
    )

    response = test_client.get(f"{MESSAGES_ROUTE_PATH}/")

    mocked_get_user_messages.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID)
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_messages__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    mocked_get_user_messages = mocker.patch(
        "app.api.routes.messages.message_service.get_user_messages",
        side_effect=NotFoundError(message=res.USER_NOT_FOUND),
    )

    response = test_client.get(f"{MESSAGES_ROUTE_PATH}/")

    mocked_get_user_messages.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID)
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}


def test_create_message_for_user__message_created__new_message_with_id_returned(
    mocker, test_client, mock_session
):
    message_create = {
        "content": "Hey there!",
    }
    mock_message_create = MessageCreate(**message_create)
    expected_message = {
        **message_create,
        "id": "ed7f6f47-487d-4e09-977e-5ecc85cc3654",
        "timestamp": "2021-08-01T00:00:00Z",
        "sender_id": USER_ID,
    }
    mock_message = Message(**expected_message)

    mocked_create_message_for_user = mocker.patch(
        "app.api.routes.messages.message_service.create_message_for_user",
        return_value=mock_message,
    )

    response = test_client.post(f"{MESSAGES_ROUTE_PATH}/", json=message_create)

    mocked_create_message_for_user.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID), message_in=mock_message_create
    )
    assert response.status_code == 200
    assert response.json() == expected_message


def test_create_message_for_user__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    message_create = {
        "content": "Hey there!",
    }
    mock_message = MessageCreate(**message_create)
    mocked_create_message_for_user = mocker.patch(
        "app.api.routes.messages.message_service.create_message_for_user",
        side_effect=NotFoundError(res.USER_NOT_FOUND),
    )

    response = test_client.post(f"{MESSAGES_ROUTE_PATH}/", json=message_create)

    mocked_create_message_for_user.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID), message_in=mock_message
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}


def test_delete_message_for_user__message_deleted__success_response(
    mocker, test_client, mock_session
):
    message_id = "ed7f6f47-487d-4e09-977e-5ecc85cc3654"
    mocked_delete_message_for_user = mocker.patch(
        "app.api.routes.messages.message_service.delete_message_for_user"
    )

    response = test_client.delete(f"{MESSAGES_ROUTE_PATH}/{message_id}")

    mocked_delete_message_for_user.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID), message_id=UUID(message_id)
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Message deleted successfully."}


def test_delete_message_for_user__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    message_id = "ed7f6f47-487d-4e09-977e-5ecc85cc3654"
    mocked_delete_message_for_user = mocker.patch(
        "app.api.routes.messages.message_service.delete_message_for_user",
        side_effect=NotFoundError(res.USER_NOT_FOUND),
    )

    response = test_client.delete(f"{MESSAGES_ROUTE_PATH}/{message_id}")

    mocked_delete_message_for_user.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID), message_id=UUID(message_id)
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}


def test_delete_message_for_user__message_not_found__404_error_response(
    mocker, test_client, mock_session
):
    message_id = "ed7f6f47-487d-4e09-977e-5ecc85cc3654"
    mocked_delete_message_for_user = mocker.patch(
        "app.api.routes.messages.message_service.delete_message_for_user",
        side_effect=NotFoundError(res.MESSAGE_NOT_FOUND),
    )

    response = test_client.delete(f"{MESSAGES_ROUTE_PATH}/{message_id}")

    mocked_delete_message_for_user.assert_called_once_with(
        session=mock_session, user_id=UUID(USER_ID), message_id=UUID(message_id)
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.MESSAGE_NOT_FOUND}

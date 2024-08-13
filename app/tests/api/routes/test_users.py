from uuid import UUID
import pytest

from app.core.constants import DEFAULT_USER_LIMIT
from app.services.exceptions import NotFoundError, AlreadyExistsError
from app.models import User
from app.models.user import UserCreate, UserUpdate
import app.core.resources as res

USERS_ROUTE_PATH = "/users"


def test_get_users__users_found__users_returned(mocker, test_client, mock_session):
    expected_users = [
        {
            "email": "user1@test.com",
            "id": "b6f37031-672d-4770-b6e8-ca34fad01968",
            "name": "User 1",
        },
        {
            "email": "user2@test.com",
            "id": "c735b48b-10ce-4ab6-8afe-d95c0e5d0a02",
            "name": "User 2",
        },
    ]
    mock_users = [User(**expected_users[0]), User(**expected_users[1])]

    mocked_get_users = mocker.patch(
        "app.api.routes.users.user_service.get_users", return_value=mock_users
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/")

    mocked_get_users.assert_called_once_with(
        limit=DEFAULT_USER_LIMIT, session=mock_session
    )
    assert response.status_code == 200
    assert response.json() == expected_users


def test_get_users__users_not_found__empty_list_returned(
    mocker, test_client, mock_session
):
    mock_users = []
    mocked_get_users = mocker.patch(
        "app.api.routes.users.user_service.get_users", return_value=mock_users
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/")

    mocked_get_users.assert_called_once_with(
        limit=DEFAULT_USER_LIMIT, session=mock_session
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_users__users_called_with_custom_limit__limited_users_returned(
    mocker, test_client, mock_session
):
    custom_limit = 1
    mocked_get_users = mocker.patch(
        "app.api.routes.users.user_service.get_users", return_value=[]
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/?limit={custom_limit}")

    mocked_get_users.assert_called_once_with(limit=custom_limit, session=mock_session)
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_by_email__user_found__user_returned(
    mocker, test_client, mock_session
):
    user_email = "user1@test.com"
    expected_user = {
        "email": user_email,
        "id": "b6f37031-672d-4770-b6e8-ca34fad01968",
        "name": "User 1",
    }
    mock_user = User(**expected_user)
    mocked_get_user_by_email = mocker.patch(
        "app.api.routes.users.user_service.get_user_by_email", return_value=mock_user
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/{user_email}")
    mocked_get_user_by_email.assert_called_once_with(
        email=user_email, session=mock_session
    )
    assert response.status_code == 200
    assert response.json() == expected_user


@pytest.mark.parametrize(
    "user_email", ["user@test", "user.com", "user@.com", f"{'u'*255}@test.com"]
)
def test_get_user_by_email__wrong_user_email_format__400_validation_error_response(
    mocker, test_client, mock_session, user_email
):
    mocked_get_user_by_email = mocker.patch(
        "app.api.routes.users.user_service.get_user_by_email"
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/{user_email}")
    mocked_get_user_by_email.assert_not_called()

    # Error messages can also be checked in the response body
    # to ensure the correct validation error handling
    assert response.status_code == 400


def test_get_user_by_email__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    user_email = "user@test.com"
    mocked_get_user_by_email = mocker.patch(
        "app.api.routes.users.user_service.get_user_by_email",
        side_effect=NotFoundError(res.USER_NOT_FOUND),
    )

    response = test_client.get(f"{USERS_ROUTE_PATH}/{user_email}")
    mocked_get_user_by_email.assert_called_once_with(
        email=user_email, session=mock_session
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}


def test_create_user__user_created__new_user_with_id_returned(
    mocker, test_client, mock_session
):
    user_create = {
        "email": "user1@test.com",
        "name": "User 1",
    }
    mock_user_create = UserCreate(**user_create)
    expected_user = {**user_create, "id": "b6f37031-672d-4770-b6e8-ca34fad01968"}
    mock_user = User(**expected_user)

    mocked_create_user = mocker.patch(
        "app.api.routes.users.user_service.create_user", return_value=mock_user
    )

    response = test_client.post(f"{USERS_ROUTE_PATH}/", json=user_create)

    mocked_create_user.assert_called_once_with(
        session=mock_session, user_in=mock_user_create
    )
    assert response.status_code == 200
    assert response.json() == expected_user


def test_create_user__email_already_exists__409_error_response(
    mocker, test_client, mock_session
):
    user_create = {
        "email": "user1@test.com",
        "name": "User 1",
    }
    mock_user = UserCreate(**user_create)
    mocked_create_user = mocker.patch(
        "app.api.routes.users.user_service.create_user",
        side_effect=AlreadyExistsError(res.EMAIL_ALREADY_EXISTS),
    )

    response = test_client.post(f"{USERS_ROUTE_PATH}/", json=user_create)

    mocked_create_user.assert_called_once_with(session=mock_session, user_in=mock_user)
    assert response.status_code == 409
    assert response.json() == {"message": res.EMAIL_ALREADY_EXISTS}


def test_update_user__user_updated__updated_user_returned(
    mocker, test_client, mock_session
):
    user_id = "b6f37031-672d-4770-b6e8-ca34fad01968"
    user_update = {
        "email": "user1@test.com",
        "name": "User 1",
    }
    mock_user_update = UserUpdate(**user_update)
    mock_user = User(**user_update, id=user_id)
    expected_user = {**user_update, "id": user_id}

    mocked_update_user = mocker.patch(
        "app.api.routes.users.user_service.update_user", return_value=mock_user
    )

    response = test_client.patch(f"{USERS_ROUTE_PATH}/{user_id}", json=user_update)

    mocked_update_user.assert_called_once_with(
        session=mock_session, user_id=UUID(user_id), user_in=mock_user_update
    )
    assert response.status_code == 200
    assert response.json() == expected_user


def test_update_user__wrong_uuid_format__400_validation_error_response(
    mocker, test_client, mock_session
):
    user_id = "123"
    mocked_update_user = mocker.patch("app.api.routes.users.user_service.update_user")

    response = test_client.patch(f"{USERS_ROUTE_PATH}/{user_id}", json={})

    mocked_update_user.assert_not_called()
    assert response.status_code == 400
    assert response.json() == {
        "detail": [
            "path -> user_id: Input should be a valid UUID, invalid length: "
            "expected length 32 for simple format, found 3"
        ]
    }


def test_update_user__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    user_id = "b6f37031-672d-4770-b6e8-ca34fad01968"
    user_update = {
        "email": "user1@test.com",
        "name": "User 1",
    }
    mock_user = UserUpdate(**user_update)
    mocked_update_user = mocker.patch(
        "app.api.routes.users.user_service.update_user",
        side_effect=NotFoundError(res.USER_NOT_FOUND),
    )

    response = test_client.patch(f"{USERS_ROUTE_PATH}/{user_id}", json=user_update)

    mocked_update_user.assert_called_once_with(
        session=mock_session, user_id=UUID(user_id), user_in=mock_user
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}


def test_update_user__email_already_exists__409_error_response(
    mocker, test_client, mock_session
):
    user_id = "b6f37031-672d-4770-b6e8-ca34fad01968"
    user_update = {
        "email": "user1@test.com",
        "name": "User 1",
    }
    mock_user = UserUpdate(**user_update)
    mocked_update_user = mocker.patch(
        "app.api.routes.users.user_service.update_user",
        side_effect=AlreadyExistsError(res.EMAIL_ALREADY_EXISTS),
    )

    response = test_client.patch(f"{USERS_ROUTE_PATH}/{user_id}", json=user_update)

    mocked_update_user.assert_called_once_with(
        session=mock_session, user_id=UUID(user_id), user_in=mock_user
    )
    assert response.status_code == 409
    assert response.json() == {"message": res.EMAIL_ALREADY_EXISTS}


def test_delete_user__user_deleted__200_response_with_success_message(
    mocker, test_client, mock_session
):
    user_id = "b6f37031-672d-4770-b6e8-ca34fad01968"
    mocked_delete_user = mocker.patch("app.api.routes.users.user_service.delete_user")

    response = test_client.delete(f"{USERS_ROUTE_PATH}/{user_id}")

    mocked_delete_user.assert_called_once_with(
        session=mock_session, user_id=UUID(user_id)
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully."}


def test_delete_user__user_not_found__404_error_response(
    mocker, test_client, mock_session
):
    user_id = "b6f37031-672d-4770-b6e8-ca34fad01968"
    mocked_delete_user = mocker.patch(
        "app.api.routes.users.user_service.delete_user",
        side_effect=NotFoundError(res.USER_NOT_FOUND),
    )

    response = test_client.delete(f"{USERS_ROUTE_PATH}/{user_id}")

    mocked_delete_user.assert_called_once_with(
        session=mock_session, user_id=UUID(user_id)
    )
    assert response.status_code == 404
    assert response.json() == {"message": res.USER_NOT_FOUND}

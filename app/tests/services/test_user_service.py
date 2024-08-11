import pytest

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models.user import UserCreate, User, UserUpdate
from app.services.user_service import (
    get_users,
    create_user,
    get_user_by_email,
    _get_user_by_email,
    get_user_by_id,
    update_user,
    delete_user,
)
from app.tests.utils import generate_random_name, generate_random_email, generate_uuid
import app.core.resources as res


def test_create_user__user_created__user_returned(session):
    email = generate_random_email()
    name = generate_random_name()
    user = create_user(session=session, user_in=UserCreate(email=email, name=name))

    assert user.email == email
    assert user.name == name
    assert user.id is not None
    assert user.messages == []


def test_create_user__user_email_already_exists__already_exists_error_raised(session):
    email = generate_random_email()
    name = generate_random_name()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()

    # Create user with the same email
    with pytest.raises(AlreadyExistsError) as err:
        create_user(session=session, user_in=UserCreate(email=email, name=name))

    assert err.value.message == res.EMAIL_ALREADY_EXISTS


def test_get_users__no_users_found__empty_list_returned(session):
    result = get_users(session=session)
    assert result == []


def test_get_users__users_found__users_returned(session):
    user1 = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )
    user2 = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )

    result_users = get_users(session=session)

    assert len(result_users) == 2
    assert user1 in result_users
    assert user2 in result_users


def test_get_user_by_email__user_found__user_returned(session):
    email = generate_random_email()
    name = generate_random_name()
    user = create_user(session=session, user_in=UserCreate(email=email, name=name))

    result_user = get_user_by_email(session=session, email=email)

    assert result_user.email == email
    assert result_user.name == name
    assert result_user.id == user.id


def test_get_user_by_email__user_not_found__not_found_error_raised(session):
    email = generate_random_email()

    with pytest.raises(NotFoundError) as err:
        get_user_by_email(session=session, email=email)

    assert err.value.message == res.USER_NOT_FOUND


def test__get_user_by_email__user_found__user_returned(session):
    email = generate_random_email()
    name = generate_random_name()
    user = create_user(session=session, user_in=UserCreate(email=email, name=name))

    result_user = _get_user_by_email(session=session, email=email)

    assert result_user.email == email
    assert result_user.name == name
    assert result_user.id == user.id


def test__get_user_by_email__user_not_found__none_returned(session):
    email = generate_random_email()

    result_user = _get_user_by_email(session=session, email=email)

    assert result_user is None


def test_get_user_by_id__user_found__user_returned(session):
    email = generate_random_email()
    name = generate_random_name()
    user = create_user(session=session, user_in=UserCreate(email=email, name=name))

    result_user = get_user_by_id(session=session, user_id=user.id)

    assert result_user.email == email
    assert result_user.name == name
    assert result_user.id == user.id


def test_get_user_by_id__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        get_user_by_id(session=session, user_id=user_id)

    assert err.value.message == res.USER_NOT_FOUND


CURRENT_USER_EMAIL = generate_random_email()
CURRENT_USER_NAME = generate_random_name()
NEW_USER_EMAIL = generate_random_email()
NEW_USER_NAME = generate_random_name()


@pytest.mark.parametrize(
    "new_email, new_name, expected_email, expected_name, user_update",
    [
        (
            NEW_USER_EMAIL,
            NEW_USER_NAME,
            NEW_USER_EMAIL,
            NEW_USER_NAME,
            UserUpdate(email=NEW_USER_EMAIL, name=NEW_USER_NAME),
        ),
        (
            NEW_USER_EMAIL,
            None,
            NEW_USER_EMAIL,
            CURRENT_USER_NAME,
            UserUpdate(email=NEW_USER_EMAIL),
        ),
        (
            None,
            NEW_USER_NAME,
            CURRENT_USER_EMAIL,
            NEW_USER_NAME,
            UserUpdate(name=NEW_USER_NAME),
        ),
        (None, None, CURRENT_USER_EMAIL, CURRENT_USER_NAME, UserUpdate()),
    ],
    ids=[
        "email_and_name_provided",
        "email_provided",
        "name_provided",
        "no_data_provided",
    ],
)
def test_update_user__user_found__user_updated(
    session, new_email, new_name, expected_email, expected_name, user_update
):
    user = create_user(
        session=session,
        user_in=UserCreate(email=CURRENT_USER_EMAIL, name=CURRENT_USER_NAME),
    )
    updated_user = update_user(session=session, user_id=user.id, user_in=user_update)

    assert updated_user.email == expected_email
    assert updated_user.name == expected_name
    assert updated_user.id == user.id


def test_update_user__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        update_user(session=session, user_id=user_id, user_in=UserUpdate())

    assert err.value.message == res.USER_NOT_FOUND


def test_update_user__user_email_already_exists__already_exists_error_raised(session):
    current_email = generate_random_email()
    name = generate_random_name()
    new_email = generate_random_email()
    user = create_user(
        session=session, user_in=UserCreate(email=current_email, name=name)
    )
    new_user = create_user(
        session=session, user_in=UserCreate(email=new_email, name=name)
    )

    with pytest.raises(AlreadyExistsError) as err:
        update_user(
            session=session, user_id=user.id, user_in=UserUpdate(email=new_email)
        )

    assert err.value.message == res.EMAIL_ALREADY_EXISTS
    assert user.id != new_user.id


def test_delete_user__user_found__user_deleted(session):
    user = create_user(
        session=session,
        user_in=UserCreate(email=generate_random_email(), name=generate_random_name()),
    )

    delete_user(session=session, user_id=user.id)

    with pytest.raises(NotFoundError) as err:
        get_user_by_id(session=session, user_id=user.id)

    assert err.value.message == res.USER_NOT_FOUND


def test_delete_user__user_not_found__not_found_error_raised(session):
    user_id = generate_uuid()

    with pytest.raises(NotFoundError) as err:
        delete_user(session=session, user_id=user_id)

    assert err.value.message == res.USER_NOT_FOUND

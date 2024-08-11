import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_session
from app.main import app
from unittest.mock import Mock


@pytest.fixture(scope="module")
def mock_session():
    return Mock()


@pytest.fixture(scope="module")
def test_client(mock_session):
    def get_session_override():
        return mock_session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

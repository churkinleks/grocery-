import pytest


@pytest.fixture
def auth_user(client, user):
    client.force_login(user)
    return user

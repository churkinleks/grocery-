import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_auth_simple_user(api_client, user):
    api_client.force_login(user)
    return user


@pytest.fixture
def api_auth_staff_user(api_client, user_factory):
    new_staff_user = user_factory(is_staff=True)
    api_client.force_login(new_staff_user)
    return new_staff_user


@pytest.fixture
def api_auth_superuser(api_client, user_factory):
    new_superuser = user_factory(is_superuser=True, is_staff=True)
    api_client.force_login(new_superuser)
    return new_superuser

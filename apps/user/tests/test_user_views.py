import pytest
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.parametrize(
    "reverse_url, status_code",
    [
        ('register', status.HTTP_200_OK),
        ('login', status.HTTP_200_OK),
        ('logout', status.HTTP_302_FOUND),
    ],
)
def test_render_views(client, reverse_url, status_code):
    response = client.get(reverse(f'user:{reverse_url}'))
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password1, password2, email, status_code, count",
    [
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', 'alex@gmail.com', status.HTTP_302_FOUND, 1),
        ('Aleksei', '12ddDS34_2', '12ddDS34_1', 'alex@gmail.com', status.HTTP_200_OK, 0),
        ('Aleksei', '12345', '12345', 'alex@gmail.com', status.HTTP_200_OK, 0),
        ('Aleksei', '123456789', '123456789', 'alex@gmail.com', status.HTTP_200_OK, 0),
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', 'alex@gmail.', status.HTTP_200_OK, 0),
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', 'alex@gmail', status.HTTP_200_OK, 0),
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', 'alex@', status.HTTP_200_OK, 0),
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', 'alex', status.HTTP_200_OK, 0),
        ('Aleksei', '12ddDS34_2', '12ddDS34_2', '', status.HTTP_200_OK, 0),
        ('Aleksei', '', '', 'alex@gmail.com', status.HTTP_200_OK, 0),
        ('', '12ddDS34_2', '12ddDS34_2', 'alex@gmail.com', status.HTTP_200_OK, 0),
    ],
)
def test_register_view(client, username, password1, password2, email, status_code, count):
    payload = {
        'username': username,
        'password1': password1,
        'password2': password2,
        'email': email,
    }
    response = client.post(reverse('user:register'), payload)

    assert response.status_code == status_code
    assert get_user_model().objects.count() == count


@pytest.mark.django_db
def test_correct_login_view(client, user):
    payload = {
        'username': user.username,
        'password': 'password',
    }
    response = client.post(reverse('user:login'), payload)

    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == (reverse('shop:dashboard'))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, password, status_code",
    [
        ('Aleksei', '12ddDS34_2', status.HTTP_200_OK),
        ('Aleksei', '123', status.HTTP_200_OK),
        ('Aleksei', '', status.HTTP_200_OK),
        ('Unreal_name', 'password', status.HTTP_200_OK),
        ('', 'password', status.HTTP_200_OK),
    ],
)
def test_incorrect_login_view(client, user, username, password, status_code):
    payload = {
        'username': username,
        'password': password,
    }
    response = client.post(reverse('user:login'), payload)
    assert response.status_code == status_code

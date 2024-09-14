import pytest
from rest_framework import status

from django.urls import reverse


@pytest.mark.django_db
class TestDetailBasket:
    def test_view(self, client, user_basket, product):
        response = client.get(reverse('basket:detail'))
        product_price = str(product.price).encode()

        assert response.status_code == status.HTTP_200_OK
        assert product.title.encode() in response.content
        assert product_price in response.content
        assert b'Total price: ' + product_price in response.content

    def test_delete_product(self, client, user_basket):
        payload = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-quantity': '20',
            'form-0-DELETE': 'on',
        }

        response = client.post(reverse('basket:detail'), payload)
        session = client.session

        assert response.status_code == status.HTTP_302_FOUND
        assert session['basket'] == {}

    def test_add_quantity(self, client, user_basket, product):
        payload = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-quantity': '20',
        }
        basket_data = {str(product.id): {'title': product.title, 'price': str(product.price), 'quantity': 20}}

        response = client.post(reverse('basket:detail'), payload)
        session = client.session

        assert response.status_code == status.HTTP_302_FOUND
        assert session['basket'] == basket_data

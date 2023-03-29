import pytest
from rest_framework import status

from django.urls import reverse


@pytest.mark.django_db
class TestDashboardView:
    def test_view(self, client, product):
        response = client.get(reverse('shop:dashboard'))

        assert response.status_code == 200
        assert product.title.encode() in response.content
        assert product.description.encode() in response.content
        assert str(product.price).encode() in response.content

    def test_purchase(self, client, auth_user, product):
        response = client.post(reverse('shop:dashboard'), {'product_id_to_purchase': product.id})
        session = client.session
        data_of_basket = {
            str(product.id): {
                'title': product.title, 'price': str(product.price), 'quantity': 1
            }}

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse('shop:dashboard')
        assert session['basket'] == data_of_basket


@pytest.mark.django_db
def test_promotion_list_view(client, promotion_factory, product):
    promotion = promotion_factory(active=True, products=[product])
    response = client.get(reverse('shop:promotion_list'))

    assert response.status_code == status.HTTP_200_OK
    assert promotion.title.encode() in response.content
    assert str(promotion.price).encode() in response.content
    assert product.title.encode() in response.content


@pytest.mark.django_db
def test_promotion_active_detail_view(client, promotion_factory):
    promotion = promotion_factory(active=True)
    response = client.get(reverse('shop:promotion_detail', args=(promotion.slug,)))

    assert response.status_code == status.HTTP_200_OK
    assert promotion.title.encode() in response.content
    assert promotion.description.encode() in response.content


@pytest.mark.django_db
def test_promotion_inactive_detail_view(client, promotion_factory):
    promotion = promotion_factory(active=False)
    response = client.get(reverse('shop:promotion_detail', args=(promotion.slug,)))
    assert response.status_code == status.HTTP_404_NOT_FOUND

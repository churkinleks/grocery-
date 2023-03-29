import pytest
from rest_framework import status

from django.urls import reverse

from apps.shop.api.serializers import CatalogSerializer, ProductSerializer, PromotionSerializer
from apps.shop.models import Product, Promotion


@pytest.mark.django_db
class TestCatalogAPI:
    endpoint_list = 'shop:catalog-list'
    endpoint_detail = 'shop:catalog-detail'

    def test_get_list(self, api_client, api_auth_simple_user, catalog_factory):
        catalog_1, catalog_2 = catalog_factory(), catalog_factory()

        response = api_client.get(reverse(self.endpoint_list))
        serialized_data = CatalogSerializer([catalog_1, catalog_2], many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_get_detail(self, api_client, api_auth_simple_user, catalog):
        response = api_client.get(reverse(self.endpoint_detail, args=(catalog.id,)))
        serialized_data = CatalogSerializer(catalog).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_post_superuser_user(self, api_client, api_auth_superuser, ):
        response = api_client.post(reverse(self.endpoint_list))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_superuser_user(self, api_client, api_auth_superuser, catalog):
        response = api_client.put(reverse(self.endpoint_detail, args=(catalog.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_superuser_user(self, api_client, api_auth_superuser, catalog):
        response = api_client.patch(reverse(self.endpoint_detail, args=(catalog.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_superuser_user(self, api_client, api_auth_superuser, catalog):
        response = api_client.delete(reverse(self.endpoint_detail, args=(catalog.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestProductAPI:
    endpoint_list = 'shop:product-list'
    endpoint_detail = 'shop:product-detail'
    
    def test_get_list(self, api_client, api_auth_simple_user, product_factory):
        product_1, product_2 = product_factory(image=None), product_factory(image=None)

        response = api_client.get(reverse(self.endpoint_list))
        serialized_data = ProductSerializer([product_1, product_2], many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_get_detail(self, api_client, api_auth_simple_user, product_factory):
        product = product_factory(image=None)
        response = api_client.get(reverse(self.endpoint_detail, args=(product.id,)))
        serialized_data = ProductSerializer(product).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_post_staff_user(self, api_client, api_auth_staff_user, catalog):
        payload = {
            'title': 'New Title',
            'price': 2.23,
            'quantity': 213,
            'description': 'Super Description',
            'catalog': catalog.id,
        }
        response = api_client.post(reverse(self.endpoint_list), payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1

    def test_put_staff_user(self, api_client, api_auth_staff_user, product, catalog):
        payload = {
            'title': 'New Title',
            'price': 2.23,
            'quantity': 213,
            'description': 'Super Description',
            'catalog': catalog.id,
        }
        response = api_client.put(reverse(self.endpoint_detail, args=(product.id,)), payload)

        assert response.status_code == status.HTTP_200_OK
        assert Product.objects.count() == 1

    def test_patch_staff_user(self, api_client, api_auth_staff_user, product):
        payload = {
            'title': 'New Title',
            'description': 'Super Description',
        }
        response = api_client.patch(reverse(self.endpoint_detail, args=(product.id,)), payload)

        assert response.status_code == status.HTTP_200_OK
        assert Product.objects.count() == 1

    def test_delete_staff_user(self, api_client, api_auth_staff_user, product):
        response = api_client.delete(reverse(self.endpoint_detail, args=(product.id,)))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0

    def test_post_simple_user(self, api_client, api_auth_simple_user):
        response = api_client.post(reverse(self.endpoint_list))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_put_simple_user(self, api_client, api_auth_simple_user, product):
        response = api_client.put(reverse(self.endpoint_detail, args=(product.id,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_patch_simple_user(self, api_client, api_auth_simple_user, product):
        response = api_client.patch(reverse(self.endpoint_detail, args=(product.id,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_simple_user(self, api_client, api_auth_simple_user, product):
        response = api_client.delete(reverse(self.endpoint_detail, args=(product.id,)))
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestPromotionAPI:
    endpoint_list = 'shop:promotion-list'
    endpoint_detail = 'shop:promotion-detail'
    
    def test_get_active_list(self, api_client, api_auth_simple_user, promotion_factory):
        promotion_1, promotion_2 = promotion_factory(active=True), promotion_factory(active=True)

        response = api_client.get(reverse(self.endpoint_list))
        serialized_data = PromotionSerializer([promotion_1, promotion_2], many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_get_active_detail(self, api_client, api_auth_simple_user, promotion_factory):
        promotion = promotion_factory(active=True)
        response = api_client.get(reverse(self.endpoint_detail, args=(promotion.id,)))
        serialized_data = PromotionSerializer(promotion).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_get_inactive_list(self, api_client, api_auth_simple_user, promotion_factory):
        promotion_1, _ = promotion_factory(active=True), promotion_factory(active=False)

        response = api_client.get(reverse(self.endpoint_list))
        serialized_data = PromotionSerializer([promotion_1], many=True).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data == serialized_data

    def test_get_inactive_detail(self, api_client, api_auth_simple_user, promotion_factory):
        promotion = promotion_factory(active=False)
        response = api_client.get(reverse(self.endpoint_detail, args=(promotion.id,)))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_post_superuser_user(self, api_client, api_auth_superuser):
        response = api_client.post(reverse(self.endpoint_list))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_put_superuser_user(self, api_client, api_auth_superuser, promotion):
        response = api_client.put(reverse(self.endpoint_detail, args=(promotion.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_superuser_user(self, api_client, api_auth_superuser, promotion):
        response = api_client.patch(reverse(self.endpoint_detail, args=(promotion.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_superuser_user(self, api_client, api_auth_superuser, promotion):
        response = api_client.delete(reverse(self.endpoint_detail, args=(promotion.id,)))
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

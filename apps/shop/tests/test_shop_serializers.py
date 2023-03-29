import pytest
from apps.shop.api.serializers import (CatalogSerializer,
                                       ProductSerializer,
                                       PromotionSerializer)


@pytest.mark.django_db
class TestCatalogSerializer:
    def test_serialize_correct_instances(self, catalog_factory, catalog):
        catalog = catalog_factory(upper_catalog=catalog)
        serialized_data = CatalogSerializer(catalog).data
        expected_data = {
            'id': catalog.id,
            'title': catalog.title,
            'upper_catalog': catalog.upper_catalog.id
        }
        assert serialized_data == expected_data


@pytest.mark.django_db
class TestProductSerializer:
    def test_serialize_correct_instances(self, product_factory):
        product = product_factory()
        serialized_data = ProductSerializer(product).data
        expected_data = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'quantity': product.quantity,
            'catalog': product.catalog.id,
            'price': str(product.price),
            'image': product.image.url,
            'specification': product.specification.url if product.specification else None
        }
        assert serialized_data == expected_data


@pytest.mark.django_db
class TestPromotionSerializer:
    def test_serialize_correct_instances(self, promotion_factory):
        promotion = promotion_factory()
        serialized_data = PromotionSerializer(promotion).data
        expected_data = {
            'id': promotion.id,
            'title': promotion.title,
            'description': promotion.description,
            'products': [product.id for product in promotion.products.all()],
            'active': promotion.active,
            'price': str(promotion.price),
            'slug': promotion.slug
        }
        assert serialized_data == expected_data

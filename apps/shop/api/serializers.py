from decimal import Decimal

from rest_framework.serializers import (
    BooleanField,
    CharField,
    DecimalField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    SlugField,
)

from apps.shop.models import Catalog, Product, Promotion


class CatalogSerializer(ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PromotionSerializer(Serializer):
    """
    These fields completely simulate the behavior of serializers.ModelSerializer (This is a portfolio)
    But this serializer doesn't provide method save and so on
    """

    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=50)
    description = CharField()
    active = BooleanField(required=False)
    price = DecimalField(decimal_places=2, max_digits=6, min_value=Decimal(0))
    slug = SlugField(allow_unicode=False, max_length=100, required=False)
    products = PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Product.objects.all())

    class Meta:
        model = Promotion

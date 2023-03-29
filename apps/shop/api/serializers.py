from rest_framework import serializers

from ..models import Catalog, Product, Promotion


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PromotionSerializer(serializers.Serializer):
    """
    These fields completely simulate the behavior of serializers.ModelSerializer (This is a portfolio)
    But this serializer doesn't provide method save and so on
    """
    id = serializers.IntegerField(label='ID', read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField()
    active = serializers.BooleanField(required=False)
    price = serializers.DecimalField(decimal_places=2, max_digits=6, min_value=0)
    slug = serializers.SlugField(allow_unicode=False, max_length=100, required=False)
    products = serializers.PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Product.objects.all())

    class Meta:
        model = Promotion

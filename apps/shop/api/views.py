from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from apps.shop.api.permissions import IsStaffOrReadOnly
from apps.shop.api.serializers import (
    CatalogSerializer,
    ProductSerializer,
    PromotionSerializer,
)
from apps.shop.models import Catalog, Product, Promotion


class CatalogAPIModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class ProductAPIModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'quantity']


class PromotionAPIModelViewSet(viewsets.ViewSet):
    """Actually we can just use ReadOnlyModelViewSet, but I did it this way for variety (This is a portfolio)"""

    queryset = Promotion.objects.all()
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):
        queryset: QuerySet[Promotion] = self.get_queryset()
        serializer: PromotionSerializer = PromotionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset: QuerySet[Promotion] = self.get_queryset()
        promotion: Promotion = get_object_or_404(queryset, pk=pk)
        serializer: PromotionSerializer = PromotionSerializer(promotion)
        return Response(serializer.data)

    def get_queryset(self) -> QuerySet[Promotion]:
        user = self.request.user
        prefetch_for_products = Prefetch('products', queryset=Product.objects.all().only('id'))
        if not user.is_staff:
            return self.queryset.filter(active=True).prefetch_related(prefetch_for_products)
        return self.queryset.prefetch_related(prefetch_for_products)

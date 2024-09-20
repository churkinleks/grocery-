from rest_framework import routers

from django.urls import include, path

from apps.shop import views
from apps.shop.api.views import (
    CatalogAPIModelViewSet,
    ProductAPIModelViewSet,
    PromotionAPIModelViewSet,
)

app_name = 'shop'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('promotions', views.promotions, name='promotions'),
    path('promotions/<slug:slug>', views.promotions_detail, name='promotions_detail'),
]

# ----- API -----
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'catalogs', CatalogAPIModelViewSet, basename='catalog')
router.register(r'products', ProductAPIModelViewSet, basename='product')
router.register(r'promotions', PromotionAPIModelViewSet, basename='promotion')

urlpatterns += [
    path('shop/api/v1/', include(router.urls)),
]

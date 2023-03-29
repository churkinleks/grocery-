from rest_framework import routers

from django.urls import path, include

from .views import DashboardView, promotion_list_view, promotion_detail_view
from .api.views import CatalogAPIModelViewSet, ProductAPIModelViewSet, PromotionAPIModelViewSet


app_name = 'shop'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('promotions', promotion_list_view, name='promotion_list'),
    path('promotions/<slug:slug>', promotion_detail_view, name='promotion_detail'),
]

# ----- API -----
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'catalogs', CatalogAPIModelViewSet, basename='catalog')
router.register(r'products', ProductAPIModelViewSet, basename='product')
router.register(r'promotions', PromotionAPIModelViewSet, basename='promotion')

urlpatterns += [
    path('shop/api/v1/', include(router.urls)),
]

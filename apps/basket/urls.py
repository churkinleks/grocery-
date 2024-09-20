from django.urls import path

from apps.basket.views import detail_basket

app_name = 'basket'

urlpatterns = [
    path('', detail_basket, name='detail'),
]

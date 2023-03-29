from django.urls import path

from .views import detail_basket

app_name = 'basket'

urlpatterns = [
    path('', detail_basket, name='detail'),
]

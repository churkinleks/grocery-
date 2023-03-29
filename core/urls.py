from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from .yasg import urlpatterns as urlpatterns_yasg

from . import settings

urlpatterns = [
    path('', include('apps.shop.urls')),
    path('user/', include('apps.user.urls')),
    path('basket/', include('apps.basket.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ----- API -----
urlpatterns += [
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/token-auth/', include('djoser.urls')),
    re_path(r'^token-auth/', include('djoser.urls.authtoken')),
]

urlpatterns += urlpatterns_yasg
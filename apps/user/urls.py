from django.contrib.auth import views as auth_views
from django.urls import path

from apps.user import views as user_views

app_name = 'user'

urlpatterns = [
    path('register', user_views.RegisterFormView.as_view(), name='register'),
    path('login', user_views.CustomLoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]

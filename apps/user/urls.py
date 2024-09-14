from django.contrib.auth import views as auth_views
from django.urls import path

from .views import RegisterFormView

app_name = 'user'

urlpatterns = [
    path('register', RegisterFormView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]

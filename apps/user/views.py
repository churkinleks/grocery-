from typing import TYPE_CHECKING

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.user.forms import CustomUserCreationForm

if TYPE_CHECKING:
    from apps.user.models import User


class RegisterFormView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('shop:dashboard')

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponseRedirect:
        user: User = form.save()
        login(self.request, user)
        form.send_email()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'user/login.html'

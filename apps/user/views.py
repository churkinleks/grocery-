from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.generic import FormView

from .forms import CustomUserCreationForm


class RegisterFormView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        form.send_email()
        return redirect('shop:dashboard')

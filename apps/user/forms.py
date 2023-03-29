from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

from .tasks import send_feedback_email_task


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        """
        Checking for email availability
        """
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists'))
        return email

    def send_email(self):
        """
        Uncomment the code below for testing Celery
        """
        pass
        # send_feedback_email_task.delay(
        #     self.cleaned_data['email'],
        #     'You have successfully registered',
        # )

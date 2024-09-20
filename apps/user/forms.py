from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (*UserCreationForm.Meta.fields, 'email')

    def clean_email(self) -> str:
        """Checking for Email availability"""
        email: str = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(_('A user with this Email already exists.'))
        return email

    def send_email(self) -> None:
        """Uncomment the code below for testing Celery"""

        # TODO(Aleksei Churkin): Check that code below works correclty

        # send_feedback_email_task.delay(
        #     self.cleaned_data['email'],
        #     'You have successfully registered',
        # )

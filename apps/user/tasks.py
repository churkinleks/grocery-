from time import sleep

from celery import shared_task

from django.core.mail import send_mail

# TODO(Aleksei Churkin): Check code below.


@shared_task()
def send_feedback_email_task(email_address: str, message: str) -> None:
    sleep(5)  # Simulate expensive operation that freeze Django
    send_mail(
        'Registration',
        f'\t{message}\n\nThank you!',
        'support@grocery.com',
        [email_address],
        fail_silently=False,
    )

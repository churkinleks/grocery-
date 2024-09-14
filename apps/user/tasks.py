from time import sleep

from celery import shared_task

from django.core.mail import send_mail


@shared_task()
def send_feedback_email_task(email_address, message):
    sleep(5)  # Simulate expensive operation that freeze Django
    send_mail(
        'Registration',
        f'\t{message}\n\nThank you!',
        'support@grocery.com',
        [email_address],
        fail_silently=False,
    )

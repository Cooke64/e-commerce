from django.conf import settings
from django.core.mail import EmailMessage


def send_email(email, message):
    """Отправляет сообщение на емейл при завершении заказа."""
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{email}'])
    return email

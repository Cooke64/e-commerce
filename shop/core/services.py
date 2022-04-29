import random
import string
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage


def generate_code():
    """Генерирует случайны код из букв, цифр. Через цикл получаем строку, с кодом."""
    alphabet = string.digits + string.ascii_uppercase + string.ascii_letters
    code_to = str()
    for i in random.sample(alphabet, 6):
        code_to += i
    return code_to


def send_email(email, message):
    """Отправляет сообщение на емейл при завершении заказа."""
    try:
        email = EmailMessage(
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[f'{email}']
        )
        return email.send()
    except SMTPException as e:
        raise

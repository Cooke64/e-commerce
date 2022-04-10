import string
import random

from django.conf import settings
from django.core.mail import EmailMessage


def generate_code():
    """Генерирует случайны код из букв, цифр. Через цикл получаем строку,
    которая сохраняется в бд и отправляется пользователю.
    """
    alphabet = string.digits + string.ascii_uppercase + string.ascii_letters
    code_to = str()
    for i in random.sample(alphabet, 6):
        code_to += i
    return code_to


def send_confirm_messages(username, email, code):
    """Отправляет сообщение на емейл для подтверждения учетной записи."""
    message = (f'Уважаемый {username},'
               f'для подтверждения вашей учетной записи перейдите по ссылке'
               f'some kind of link/'
               f'укажите этот код {code}')
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{email}'])
    return email.send()

import random
import string

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage

from coupons.models import Coupon
# from customer.services import generate_code


def generate_code():
    """Генерирует случайны код из букв, цифр. Через цикл получаем строку, с кодом."""
    alphabet = string.digits + string.ascii_uppercase + string.ascii_letters
    code_to = str()
    for i in random.sample(alphabet, 6):
        code_to += i
    return code_to

def send_email(email, message):
    """Отправляет сообщение на емейл при завершении заказа."""
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{email}']
    )
    return email.send()


def generate_promocode():
    """Создает промокод для скидки."""
    code = generate_code()
    try:
        Coupon.objects.create(code=code)
        return code
    except ObjectDoesNotExist as e:
        raise e

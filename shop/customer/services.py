import string
import random

from core.services import send_email


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
    email = send_email(email, message)
    return email.send()


def send_welcome_email(email, promocode):
    """Отправляет сообщение на емейл для подтверждения учетной записи."""
    message = (f'Поздравляем с успешной регистрацией. Дарим вам этот промокод со скидкой 5%'
               f'{promocode}')
    email = send_email(email, message)
    return email.send()

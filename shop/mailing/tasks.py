from celery import current_task

from django.conf import settings
from django.core.mail import EmailMessage

from coupons.views import generate_promocode
from customer.models import User
from mailing.models import Mailing
from shop.celery import app

CODE = generate_promocode()


def sender_messages(request, email, message):
    """Отправляет сообщение на емейл при завершении заказа."""
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{email}'])
    Mailing.objects.create(
        user=request.user,
        text=message,
        promo_code=CODE,
    )
    return email.send()


@app.task
def send_mail_to_user_without_payment(request):
    """
    Задача для отправки сообщений, если пользователь давно не производил покупки.
    """
    message = f'Что-то давно не покупали у нас. Вот вам подарочный код {CODE}'
    user = request.user.username
    if user.last_buy is None:
        return sender_messages(request, user.email, message)


@app.task
def send_mail_to_everyone(request):
    """
    Задача для отправки сообщений всем пользователям..
    """
    message = f'У нас новые товары. Загляни:)'
    users = User.objects.all().valuse('email')
    for user in users:
        return sender_messages(request, user.email, message)
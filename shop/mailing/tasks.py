from celery import current_task

from django.conf import settings
from django.core.mail import EmailMessage

from coupons.views import generate_promocode
from mailing.models import Mailing
from shop.celery import app


def sender_messages(request):
    """Отправляет сообщение на емейл при завершении заказа."""
    code = generate_promocode()
    message = f'Что-то давно не покупали у нас. Вот вам подарочный код {code}'
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{request.user.email}'])
    Mailing.objects.create(
        user=request.user,
        text=message,
        promo_code=code,
    )
    return email.send()


@app.task
def send_mail_to_user_without_payment(request):
    """
    Задача для отправки сообщений, если пользователь давно не производил покупки.
    """
    user = request.user.username
    if user.last_buy is None:
        return sender_messages(request)

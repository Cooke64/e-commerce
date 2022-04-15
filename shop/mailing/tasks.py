from core.services import send_email
from coupons.views import generate_promocode
from customer.models import User, Customer
from mailing.models import Mailing
from shop.celery import app

CODE = generate_promocode()


def sender_messages(request, email, message):
    """Создает объъект email от базовой функции отправки сообщения.
     Далее создается объект в модель отправленной рассылки."""
    email = send_email(email, message)
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
    users = Customer.objects.select_related('user').filter(last_buy=0)
    for user in users:
        return sender_messages(request, user.email, message)


@app.task
def send_mail_to_everyone(request):
    """
    Задача для отправки сообщений всем пользователям.
    """
    message = f'У нас новые товары. Загляни:)'
    users = User.objects.all().valuse('email')
    for user in users:
        return sender_messages(request, user.email, message)


@app.task
def send_welcome_email(email, promocode):
    """Отправляет сообщение на емейл для подтверждения учетной записи."""
    message = (f'Поздравляем с успешной регистрацией. Дарим вам этот промокод со скидкой 5%'
               f'{promocode}')
    return send_email(email, message)



@app.task
def send_confirm_messages(username, email, code):
    """Отправляет сообщение на емейл для подтверждения учетной записи."""
    message = (f'Уважаемый {username},'
               f'для подтверждения вашей учетной записи перейдите по ссылке'
               f'some kind of link/'
               f'укажите этот код {code}')
    return send_email(email, message)


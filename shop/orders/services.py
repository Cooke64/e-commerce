from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import F

from coupons.views import generate_promocode
from customer.models import Customer
from orders.models import OrderItem


def make_order(cart, order, request):
    """Создает в в модели OrderItem через цикл отдельный элемент всего заказа
    пользователя.
    """
    customer = Customer.objects.get(user=request.user)
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )
        customer.spent_money = F('spent_money') + item['price']
        customer.save()


def make_order_item(cart, order, request):
    """Создает в модели Order заказ пользователя, при наличии скидки
    применяет её. При завершении заказа отправляет сообщение пользователю.
    """
    order.customer = request.user
    if cart.coupon:
        order.coupon = cart.coupon
        order.discount = cart.coupon.discount
    order.save()
    make_order(cart, order, request)
    sender_messages(request, order_id=order.pk)


def sender_messages(request, order_id):
    """Отправляет сообщение на емейл при завершении заказа."""
    order = OrderItem.objects.get(id=order_id)
    user = request.user
    code = generate_promocode()
    message = f'Уважаемый {user.customer.first_name},ваш заказ #{order.pk} готовится к отправке.' \
              f'У вас подарочный промокод {code}'
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{user.email}'])
    return email.send()
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def sender_messages(request, order_id):
    """Отправляет сообщение на емейл при завершении заказа."""
    order = OrderItem.objects.get(id=order_id)
    user = request.user
    message = (f'Уважаемый {user.first_name},'
               f' ваш заказ #{order.pk} готовится к отправке.')
    email = EmailMessage(
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[f'{user.email}'])
    return email.send()


@login_required(login_url='login_user')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])

            sender_messages(request, order_id=order.pk)
            cart.clear()
            return redirect('user_profile')
    else:
        form = OrderCreateForm
    context = {
        'cart': cart, 'form': form
    }
    return render(request, 'order/order_create.html', context)

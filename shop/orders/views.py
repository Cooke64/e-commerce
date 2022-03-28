from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required(login_url='login_user')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'order/check_out.html',
                          {'order': order})
    else:
        form = OrderCreateForm

    return render(request, 'order/order_create.html',
                  {'cart': cart, 'form': form})
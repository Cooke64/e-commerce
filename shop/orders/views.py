from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from customer.models import Customer
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
                (Customer.objects
                 .filter(user=request.user)
                 .update(spent_money=F('spent_money') + (item['price'] * item['quantity']),))
            cart.clear()
            return render(request, 'index',
                          {'order': order})
    else:
        form = OrderCreateForm
    context = {
        'cart': cart, 'form': form
    }
    return render(request, 'order/order_create.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import OrderCreateForm
from cart.cart import Cart
from .services import make_order_item


@login_required(login_url='login_user')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            make_order_item(cart, order, request)
            cart.clear()
            return redirect('user_profile')
    else:
        form = OrderCreateForm
    context = {'cart': cart, 'form': form}
    return render(request, 'order/order_create.html', context)

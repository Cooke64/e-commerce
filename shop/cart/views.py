from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CouponApplyForm


@login_required(login_url='login_user')
@require_POST
def add_product_in_cart(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd['quantity'], update_quantity=cd['update']
        )
    return redirect('cart_detail')


@login_required(login_url='login_user')
def remove_product_from_cart(request, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=product_slug)
    try:
        cart.remove(product)
        return redirect('cart_detail')
    except ObjectDoesNotExist as e:
        raise e


@login_required(login_url='login_user')
def get_cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True}
        )
    context = {
        'cart': cart, 'coupon_apply_form': coupon_apply_form,
    }
    return render(request, 'cart/cart_detail.html', context)

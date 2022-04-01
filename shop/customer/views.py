from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from cart.cart import Cart
from customer.forms import (
    UserRegisterForm,
    UserEditForm,
    ProfileEditForm)
from customer.models import Customer
from orders.models import OrderItem


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'customer/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')


def signup(request):
    signup_is_true = True
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            Customer.objects.create(user=user)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong')
    context = {
        'signup_is_true': signup_is_true,
        'form': form
    }
    return render(request, 'customer/login.html', context)


@login_required(login_url='login_user')
def user_profile(request):
    user = request.user
    cart = Cart(request)
    current_orders_lust = user.orders.values_list('items', flat=True)
    current_orders = OrderItem.objects.filter(order__in=current_orders_lust)
    context = {'user': user,
               'cart': cart,
               'current_orders': current_orders
               }
    return render(request, 'customer/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        customer_form = ProfileEditForm(instance=request.user.customer,
                                        data=request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        customer_form = ProfileEditForm(instance=request.user.customer)
        return render(request,
                      'customer/edit_profile.html',
                      {'user_form': user_form,
                       'profile_form': customer_form})

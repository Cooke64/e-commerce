from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from customer.forms import (
    UserRegisterForm, UserEditForm,
    ProfileEditForm, CodeForm,
)
from customer.models import Customer, User
from customer.services import generate_code, make_login_user, activate_user, \
    save_user
from orders.models import Order


def login_user(request):
    """Аутентификация пользователя."""
    if request.user.is_authenticated or request.user.is_active:
        return redirect('index')
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        make_login_user(request, form)
    return render(request, 'customer/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


def signup(request):
    """Регистрация пользователя. Дополнительно создается
    профиль пользователя, который он сможет редактировать.
    """
    if request.user.is_authenticated or request.user.is_active:
        return redirect('index')
    form = UserRegisterForm()
    # Создаем код для подтверждения по емейлу
    code = generate_code()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            save_user(user, code)
        else:
            messages.error(request, 'Something went wrong')
    context = {'signup_is_true': True, 'form': form}
    return render(request, 'customer/login.html', context)


def enter_code_to_confirm(request):
    """Подтверждение кода, полученного через емайл."""
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            activate_user(request, form)
    form = CodeForm()
    return render(request, 'customer/activate_code.html', {'form': form})


@login_required(login_url='login_user')
def user_profile(request):
    user = request.user
    order = Order.objects.filter(customer=user)
    context = {'user': user, 'cart': Cart(request), 'order': order}
    return render(request, 'customer/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        customer_form = ProfileEditForm(
            instance=request.user.ustomer, data=request.POST
        )
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect('user_profile')
    user_form = UserEditForm(instance=request.user)
    customer_form = ProfileEditForm(instance=request.user)
    return render(request, 'customer/edit_profile.html',
                      {'user_form': user_form, 'profile_form': customer_form})


@login_required
def delete_user_account(request, ):
    user_to_delete = get_object_or_404(User, id=request.user.id)
    try:
        user_to_delete.is_active = False
        user_to_delete.save()
        return redirect('index')
    except ObjectDoesNotExist as e:
        raise e


@login_required
def stop_user_being_subscribed(request):
    """Отменяем подписку на рассылку."""
    user = get_object_or_404(Customer, user_id=request.user)
    try:
        user.subscribed = False
        user.save()
        return redirect('user_profile')
    except ObjectDoesNotExist as e:
        raise e

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from customer.forms import (
    UserRegisterForm, UserEditForm,
    ProfileEditForm, CodeForm,
)
from customer.models import Customer, User
from customer.services import send_confirm_messages, generate_code
from orders.models import OrderItem


def login_user(request):
    """Аутентификация пользователя."""
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('login_user')
        try:
            login(request, user)
            return redirect('index')
        except ValidationError as e:
            raise e

    return render(request, 'customer/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


def signup(request):
    """Регистрация пользователя. Дополнительно создается
    профиль пользователя, который он сможет редактировать.
    """
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')
    signup_is_true = True
    form = UserRegisterForm()
    code = generate_code()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            if user.is_admin and user.is_staff:
                user.is_active = True
            user.is_active = False
            user.code = code
            user.save()
            Customer.objects.create(user=user)
            send_confirm_messages(username=user.username, email=user.email, code=code)
            return redirect('confirm')
        else:
            messages.error(request, 'Something went wrong')
    context = {
        'signup_is_true': signup_is_true,
        'form': form
    }
    return render(request, 'customer/login.html', context)


def enter_code_to_confirm(request):
    """Подтверждение кода, полученного через емайл."""
    if request.user.is_authenticated and request.user.is_active:
        return redirect('index')
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            sent_code_via_email = form.cleaned_data.get("code")
            try:
                user = User.objects.get(code=sent_code_via_email)
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('index')
            except ObjectDoesNotExist as error:
                raise error
    form = CodeForm()
    return render(request, 'customer/activate_code.html', {'form': form})


@login_required(login_url='login_user')
def user_profile(request):
    user = request.user
    cart = Cart(request)
    context = {'user': user,
               'cart': cart,
               }
    return render(request, 'customer/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        customer_form = ProfileEditForm(
            instance=request.user, data=request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        customer_form = ProfileEditForm(instance=request.user)
        return render(request, 'customer/edit_profile.html',
                      {'user_form': user_form, 'profile_form': customer_form})


@login_required
def delete_user_account(request, ):
    user_to_delete = get_object_or_404(User, id=request.user.id)
    user_to_delete.delete()
    messages.success(request, "Deleted")
    return redirect('index')

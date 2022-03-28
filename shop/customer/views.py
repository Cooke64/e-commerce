from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from cart.cart import Cart
from customer.forms import UserRegisterForm, UserEnterForm


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
    context = {
        'user': user,
        'cart': cart
    }
    return render(request, 'customer/profile.html', context)




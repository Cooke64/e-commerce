import string
import random

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import redirect

from customer.models import User
from mailing.tasks import send_welcome_email, send_confirm_messages


def generate_code():
    """Генерирует случайны код из букв, цифр. Через цикл получаем строку, с кодом."""
    alphabet = string.digits + string.ascii_uppercase + string.ascii_letters
    code_to = str()
    for i in random.sample(alphabet, 6):
        code_to += i
    return code_to


def make_login_user(request, form):
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


def activate_user(request, form):
    """Находим пользователя по коду, подтверждаем этого пользователя, отправляем мейл с промокодом."""
    sent_code_via_email = form.cleaned_data.get("code")
    try:
        user = User.objects.get(code=sent_code_via_email)
        user.is_active = True
        user.save()
        # Task to celery mailing
        send_welcome_email(email=user.email, promocode=123)
        login(request, user,
              backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')
    except ObjectDoesNotExist as error:
        raise error


def save_user(user, code):
    user.username = user.username
    if user.is_admin and user.is_staff:
        user.is_active = True
    user.is_active = False
    user.code = code
    user.save()
    send_confirm_messages(username=user.username, email=user.email, code=code)
    return redirect('confirm')

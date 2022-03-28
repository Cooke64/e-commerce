from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from customer.models import Customer


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserEnterForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',]


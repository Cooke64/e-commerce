from .models import Customer

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CodeForm(forms.Form):
    """Форма заполнения кода, который был отправлен по email для подтверждения учетной записи."""
    code = forms.CharField(
        label='Код', required=True, max_length=15,
        )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('phone', 'address', 'delivery_info', )


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
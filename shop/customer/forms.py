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

    def clean_confirm_password(self) -> str:
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if confirm_password != password:
            raise forms.ValidationError(message='Пароли не совпадают')
        return confirm_password


class CodeForm(forms.Form):
    """Форма заполнения кода, который был отправлен по email для подтверждения учетной записи."""
    code = forms.CharField(
        label='Код', required=True, max_length=15,
        )

    def execute(self):
        user_id = self.cleaned_data['user_id']
        user = User.objects.get(pk=user_id)
        user.active = True
        user.save()
        send_mail(...)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')


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
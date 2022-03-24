from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

User = get_user_model()


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = 'acc/login.html'
    success_message = "You are successfully logged in!"


class LogoutPage(LogoutView):
    def get_next_page(self):
        next_page = super(LogoutPage, self).get_next_page()
        return reverse('index')


class SignUpPage(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('ecom:ecom_login')
    template_name = 'acc/signup.html'
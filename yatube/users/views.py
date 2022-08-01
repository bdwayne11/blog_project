from django.views.generic import CreateView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class MyPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_success')
    template_name = 'users/password_change_form.html'


class MyPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:password_reset_success')
    template_name = 'users/password_reset_form.html'

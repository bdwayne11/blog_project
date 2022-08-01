from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'),
        name='logout'),

    path('signup/', views.SignUp.as_view(), name='signup'),

    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'
         ),

    path('password_change/',
         views.MyPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_success'),
    path(
        'password_reset/',
        views.MyPasswordResetView.as_view(),
        name='password_reset'),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_success'),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complite')),
        name='password_reset_confirm'),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
        name='password_reset_complite')
]

from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render
from django.views import View




from auth_user.forms import AuthForm


""" выход пользователя из системы """


class LogOut(LogoutView):
    template_name = "auth_user/auth.html"
    next_page = '/'

""" авторизация пользователя в системе """


class AuthenticationView(LoginView):
    template_name = 'auth_user/auth.html'
    form_class = AuthForm
    next_page = 'work_place'
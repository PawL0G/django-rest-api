from django.urls import path
from .views import login_page, register_page, redirect_to_login

urlpatterns = [
    path("", redirect_to_login),
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
]

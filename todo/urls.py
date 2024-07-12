from django.urls import path

from . import views
from django.urls import path
from . import views

from django.shortcuts import redirect

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("<int:user_id>/", views.index, name="index"),
    path("forgot/", views.forgot, name="forgot"),
    path("change/<str:username>", views.change, name="change"),
]

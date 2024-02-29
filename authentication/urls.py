from django.contrib import admin
from django.urls import path, include
from . import views
from .views import login, register, logout
urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("", views.home, name="home"),

]

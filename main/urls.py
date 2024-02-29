from django.contrib import admin
from django.urls import path
from main import views
urlpatterns = [
    path("scrape/", views.scrape, name="scrape"),
    path("delete/", views.delete, name="delete"),
]

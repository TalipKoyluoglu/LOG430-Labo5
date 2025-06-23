from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("magasin.urls")),
    path("", include("django_prometheus.urls")),
]

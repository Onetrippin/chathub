from django.contrib import admin
from django.urls import path
from authapp.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]

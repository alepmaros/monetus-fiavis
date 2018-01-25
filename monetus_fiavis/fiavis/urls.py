from django.contrib import admin
from django.urls import path, re_path

from fiavis import views

urlpatterns = [
    path('', views.index_fiavis, name='index-fiavis'),
]
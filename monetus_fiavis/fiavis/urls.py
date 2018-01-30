from django.contrib import admin
from django.urls import path, re_path

from fiavis import views

urlpatterns = [
    path('stocks/', views.stocks, name='stocks-fiavis'),
    path('', views.index_fiavis, name='index-fiavis'),
]
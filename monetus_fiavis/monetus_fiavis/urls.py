"""monetus_fiavis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    re_path(r'^$', include('fiavis.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    

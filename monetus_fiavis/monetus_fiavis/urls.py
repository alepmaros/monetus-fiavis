"""monetus_fiavis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='monetus/')),
    path('monetus/', include('fiavis.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
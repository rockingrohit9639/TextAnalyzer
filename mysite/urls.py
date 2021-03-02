"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('analyze', views.analyze, name='rmvpunc'),
    path('about', views.about, name='About Us'),
    path('index', views.home, name='Analyze Text'),
    path('index2', views.index2, name='Generate Text'),
    path('gallery/',views.gallery,name='gallery'),
]

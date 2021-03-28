from django.contrib import admin
from django.urls import path
from . import views
from .views import render_pdf_view, PdfListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('analyze', views.analyze, name='rmvpunc'),
    path('about', views.about, name='About Us'),
    path('index', views.home, name='Get Started'),
    path('index2', views.index2, name='Generate Text'),
    path('gallery/',views.gallery,name='gallery'),
    path('youtube/', views.youtube, name='youtube'),
    path('books/', views.searchBook, name='books'),
    path("contact",views.contact,name="contact"),
    path('articles/', views.articles, name='articles'),
    path('pdf/', render_pdf_view, name='pdf-view'),
    path('', PdfListView.as_view(), name='pdf-list-view'),
]


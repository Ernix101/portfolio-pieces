from django.urls import path
from . import views

# Connect/route your urls here
urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('menu/', views.menu, name='menu'),
]

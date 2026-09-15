from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('patients/', views.patients_view, name='patients'),
    path('providers/', views.providers_view, name='providers'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('profile/', views.profile_view, name='profile'),
    path('appointments/<int:appointment_id>/status/<str:new_status>/', views.update_appointment_status, name='update_status'),
    path('search/', views.search_appointments, name='search_appointments'),
]

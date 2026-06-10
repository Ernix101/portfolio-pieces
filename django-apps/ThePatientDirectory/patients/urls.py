from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('new/', views.patient_create, name='patient_create'),
    path('<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('<int:pk>/update/', views.patient_update, name='patient_update'),
]

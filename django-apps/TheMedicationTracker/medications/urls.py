from django.urls import path
from . import views

# create your app urls here

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory, name='inventory'),
    path('dosages/', views.dosage, name='dosages'),
    path('expiry/', views.expiry, name='expiry'),
    path('reports/', views.reports, name='reports'),
    
    path('list/', views.patient_list, name='patient_list'),
    path('new_patient/', views.patient_add, name='patient_add'),
    path('new_med/', views.medication_add, name='medication_add'),
    path('new_record/', views.record_add, name='record_add'),

    path('<int:pk>/', views.patient_detail, name='patient_detail'),

    path('<int:pk>/update_patient/', views.patient_update, name='patient_update'),
    path('<int:pk>/update_med/', views.med_update, name='med_update'),
    path('<int:pk>/update_record/', views.record_update, name='record_update'),

    path('<int:pk>/delete_patient/', views.patient_delete, name='patient_delete'),
    path('<int:pk>/delete_med/', views.med_delete, name='med_delete'),
    path('<int:pk>/delete_record', views.record_delete, name='record_delete'),
]

from django.contrib import admin
from .models import Department, Specialty, Patient, Provider, Appointment


# Register your models here.
admin.site.register(Provider)
admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Specialty)
admin.site.register(Appointment)

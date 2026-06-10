from django.db import models

# Create your models here.
class Patient(models.Model):
    BLOOD_TYPES = [
        ('A', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=15)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)

    def __str__(self):
        return self.name
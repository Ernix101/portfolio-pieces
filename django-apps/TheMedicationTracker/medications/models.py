from django.db import models
from django.utils import timezone

# Create your models here.
    
#* A related Patient
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date_of_birth = models.DateField(default=timezone.now)
    condition = models.CharField(max_length=200)
    demographics = models.CharField(max_length=200)
    email= models.EmailField(default='Unknown')
    allergies = models.CharField(max_length=200, default='None')
    SEX = [
        ('Male', 'Male'), ('Female', 'Female'),
    ]
    BLOOD_TYPES = [
        ('A', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    sex = models.CharField(max_length=7, choices=SEX, default='Unknown')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, default='Unknown')
    phone_no = models.IntegerField(default=0)
    register_date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.name


# * The Medication itself
class Medication(models.Model):
    name = models.CharField(max_length=100)
    batch_no = models.CharField(max_length=200, default=0)
    stock = models.IntegerField(default=0)
    expiry_date = models.DateField()

    def __str__(self):
        return self.name
    

#* The MedicationRecord linking the two models above
class MedicationRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=10)
    frequency = models.CharField(max_length=50)
    date_prescribed = models.DateField()

    def __str__(self):
        return f"{self.patient} - {self.medication}"
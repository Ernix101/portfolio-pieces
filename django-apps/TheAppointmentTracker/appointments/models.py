from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

# ! Department Model
class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ! Specialty Model (JOB)
class Specialty(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.department.code})"



 # ! Provider Model (DOCTORS) 
class Provider(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT)
    working_hours = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

    #* We want to only be able to deactivate a provider instead of delete
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ({self.specialty})"
    

# ! Patient Model (CLIENT)
class Patient(models.Model):
    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    sex = models.CharField(max_length=6, choices=SEX)
    condition = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15)

    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}- ({self.condition})"
  

# ! Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('checked_in', 'Checked In'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('no_show', 'No Show'),
    ]

    TYPE_CHOICES = [
        ('consultation', 'Consultation'),   # e.g. 30mins    
        ('follow_up', 'Follow Up'),     # e.g. 15mins
        ('checkup', 'Checkup'),
        ('referral', 'Specialist Referral'),
        ('vaccination', 'Vaccination'),
        ('procedure', 'Procedure'),      # e.g. 60mins
        ('post_procedure', 'Post Procedure'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True)
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.patient.name} with {self.provider.name} on {self.start_time}"
    
    # * Finding when an appointment will be over to set availability
    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration_minutes)

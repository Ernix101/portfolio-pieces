from django import forms
from .models import Patient
from  django.core.validators import RegexValidator

# ! Phone number validator
phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{9,15}$',
    message="Enter a valid phone number. E.g: +25412345678"
)

class PatientForm(forms.ModelForm):
    contact = forms.CharField(validators=[phone_validator])

    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'contact', 'blood_type']
        
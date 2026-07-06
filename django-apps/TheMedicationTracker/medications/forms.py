from django import forms
from .models import Patient, Medication, MedicationRecord


#* A Patient form
class PatientForm(forms.ModelForm):
     class Meta:
          model = Patient
          fields = ['name', 'age', 'sex', 'condition','phone_no', 'demographics', 'date_of_birth' ,'email', 'allergies', 'blood_type', 'register_date']

#* A Medication form
class MedicationForm(forms.ModelForm):
     class Meta:
          model = Medication
          fields = ['name', 'batch_no','stock','expiry_date']

#* MedicationRecrdForm
class MedicationRecordForm(forms.ModelForm):
     class Meta:
          model = MedicationRecord
          fields = ['patient', 'medication', 'dosage', 'frequency', 'date_prescribed']
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Medication, MedicationRecord
from .forms import PatientForm, MedicationForm, MedicationRecordForm
from django.utils import timezone
from datetime import timedelta, date
from django.db import models
import json


# Create your views here.
#! DASHBOARD view
def dashboard(request):
    today = timezone.now().date()
    thirty_days = today + timedelta(days=30)

    total_meds = Medication.objects.count()
    total_stock = Medication.objects.aggregate(total=models.Sum('stock'))['total'] or 0
    expiring_soon = Medication.objects.filter(expiry_date__range=[today, thirty_days])
    low_stock = Medication.objects.filter(stock__lt=20)
    # * Getting last seven days for each of their records
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    records_per_day = [
        MedicationRecord.objects.filter(date_prescribed=day).count()
        for day in last_7_days
    ]
    labels = [day.strftime('%b %d') for day in last_7_days]

    context = {
        'total_meds': total_meds,
        'total_stock': total_stock,
        'expiring_soon_count': expiring_soon.count(),
        'low_stock_count': low_stock.count(),
        'expiring_soon_list': expiring_soon.order_by('expiry_date')[:5],
        'recent_inventory': Medication.objects.order_by('-id')[:5],
        'total_patients': Patient.objects.count(),
        'todays_records': MedicationRecord.objects.filter(date_prescribed=date.today()).count(),
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(records_per_day),
    }
    return render(request, 'medications/dashboard.html', context)


#! INVENTORY view
def inventory(request):
    today = timezone.now().date()
    thirty_days = today + timedelta(days=30)

    medications = Medication.objects.all().order_by('-id')

    context = {
        'today': today,
        'medications': medications,
        'total_units': Medication.objects.aggregate(total=models.Sum('stock'))['total'] or 0,
        'total_meds': Medication.objects.count(),
        'low_stock': Medication.objects.filter(stock__lt=20).count(),
        'expiring_soon': Medication.objects.filter(expiry_date__range=[today, thirty_days]).count(),
    }
    return render(request, 'medications/inventory.html', context)


#! DOSAGE view
def dosage(request):
    today =  timezone.now().date()
    records = MedicationRecord.objects.all().order_by('-date_prescribed')

    context = {
        'records': records,
        'today': today,
        'total_records': records.count(),
        'todays_records': MedicationRecord.objects.filter(date_prescribed=today).count(),
        'total_patients': Patient.objects.filter(medicationrecord__isnull=False).distinct().count(),
        'unique_meds': Medication.objects.filter(medicationrecord__isnull=False).distinct().count(),
    }
    return render(request, 'medications/dosage_records.html', context)


#! EXPIRY meds view
def expiry(request):
    today = timezone.now().date()
    seven_days = today + timedelta(days=7)
    thirty_days = today + timedelta(days=30)

    critical = Medication.objects.filter(expiry_date__range=[today, seven_days])
    warning = Medication.objects.filter(expiry_date__gt=seven_days, expiry_date__lte=thirty_days)
    safe = Medication.objects.filter(expiry_date__gt=thirty_days)

    context = {
        'today': today,
        'critical': critical,
        'warning': warning,
        'critical_count': critical.count(),
        'warning_count': warning.count(),
        'safe_count': safe.count(),
        'total_meds': Medication.objects.count(),
    }
    return render(request, 'medications/expiry_alerts.html', context)



#! REPORTS view
def reports(request):
    today = timezone.now().date()
    seven_days = today + timedelta(days=7)
    thirty_days = today + timedelta(days=30)

    # * Monthly data - last 6 months
    months = []
    monthly_counts = []
    for i in range(5, -1, -1):
        month = today.replace(day=1) - timedelta(days=i*30)
        count = MedicationRecord.objects.filter(
            date_prescribed__year=month.year,
            date_prescribed__month=month.month,
        ).count()
        months.append(month.strftime('%b'))
        monthly_counts.append(count)

    context = {
        'today': today,
        'total_meds': Medication.objects.count(),
        'total_stock': Medication.objects.aggregate(total=models.Sum('stock'))['total'] or 0,
        'expiring_soon': Medication.objects.filter(expiry_date__range=[today, thirty_days]).count(),
        'expired': Medication.objects.filter(expiry_date__lte=today).count(),
        'total_patients': Patient.objects.count(),
        'total_records': MedicationRecord.objects.count(),
        'critical_count': Medication.objects.filter(expiry_date__range=[today, seven_days]).count(),
        'warning_count': Medication.objects.filter(expiry_date__gt=seven_days, expiry_date__lte=thirty_days).count(),
        'safe_count': Medication.objects.filter(expiry_date__gt=thirty_days).count(),

        'chart_labels': json.dumps(months),
        'chart_data': json.dumps(monthly_counts),
        'most_used': Medication.objects.annotate(record_count=models.Count('medicationrecord')).order_by('-record_count')[:5],

        'expiry_data': json.dumps([
            Medication.objects.filter(expiry_date__range=[today, seven_days]).count(),
            Medication.objects.filter(expiry_date__gt=seven_days, expiry_date__lte=thirty_days).count(),
            Medication.objects.filter(expiry_date__gt=thirty_days).count(),
        ])
    }
    return render(request, 'medications/reports.html', context)



#! VIEW the list
def patient_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter( name__icontains = query)
    else:
        patients = Patient.objects.all()
    return render(request, 'medications/patient_list.html', {'patients': patients, 'query': query})

#! view the patient's DETAILS
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    today = timezone.now().date()
    thirty_days = today + timedelta(days=30)

    records = MedicationRecord.objects.filter(patient=patient)

    context = {
        'today': today,
        'patient': patient,
        'total_records': records.count(),
        'active_meds': records.filter(medication__expiry_date__gte=today).count(),
        'this_month': records.filter(date_prescribed__month=today.month).count(),
        'expiring_soon': records.filter(medication__expiry_date__range=[today, thirty_days]).count(),
        'records': records.order_by('-date_prescribed'),
    }
    return render(request, 'medications/patient_detail.html', context)







#! ADD a patient
def patient_add(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'medications/patient_add.html', {'form': form})


#! ADD a medication
def medication_add(request):
    if request.method == "POST":
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = MedicationForm()
    return render(request, 'medications/medication_add.html', {'form': form})


#! ADD a record for the medication and patient
def record_add(request):
    if request.method == "POST":
        form = MedicationRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', pk=form.instance.patient.pk)
    else:
        form = MedicationRecordForm()
    return render(request, 'medications/record_add.html', {'form': form})



#! UPDATE a patient
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'medications/patient_add.html', {'form': form})

#! UPDATE a medication
def med_update(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'medications/medication_add.html', {'form': form})

#! UPDATE a record
def record_update(request, pk):
    record = get_object_or_404(MedicationRecord, pk=pk)
    if request.method == 'POST':
        form = MedicationRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dosages')
    else:
        form = MedicationRecordForm(instance=record)
    return render(request, 'medications/record_add.html', {'form': form})

#! DELETE a patient
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    
    return render(request, 'medications/patient_confirm_delete.html', {'patient': patient})

#! DELETE a medication
def med_delete(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        medication.delete()
        return redirect('patient_list')
    
    return render(request, 'medications/med_confirm_delete.html', {'medication': medication})


#! DELETE a record
def record_delete(request, pk):
    record = get_object_or_404(MedicationRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('patient_list')
    
    return render(request, 'medications/record_confirm_delete.html', {'record': record})

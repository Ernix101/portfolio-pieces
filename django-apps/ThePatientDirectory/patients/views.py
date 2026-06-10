from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientForm
from django.core.paginator import Paginator

# Create your views here.
def patient_list(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter( name__icontains=query )
    else:
        patients = Patient.objects.all()

    paginator = Paginator(patients, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'patients/patient_list.html', {
        'patients': page_obj, 
        'query': query
    })

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/patient_detail.html', {'patient': patient})


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})
    

#! How you can update the existing patient
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})



# ! A way to delete the patient instance created
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})


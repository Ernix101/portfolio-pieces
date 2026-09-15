from django.shortcuts import render
from datetime import date, timedelta
from django.utils import timezone
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Appointment, Patient, Provider, Department, Specialty
from django.http import JsonResponse
from django.db.models import Q



# ------------------------------------------------Page based views and their features------------------------------------------------
# ! DASHBOARD PAGE VIEW
def dashboard_view(request):
    context = {
        'active_page': 'dashboard',
    }
    return render(request, 'appointments/dashboard.html', context)





# ! CALENDAR PAGE VIEW
def calendar_view(request):
    today = date.today()
    todays_appointments = Appointment.objects.filter(start_time__date=today)
    today_display = date.today()

    # Get data from query param, default to current week
    week_param = request.GET.get('week')
    if week_param:
        start_of_week = date.fromisoformat(week_param)
    else:
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())   # Monday

    end_of_week = start_of_week + timedelta(days=6)

    #* confirming which week is current to display in the calendar
    is_current_week = (start_of_week == today - timedelta(days=today.weekday()))

    appointments = Appointment.objects.filter(
        start_time__date__gte=start_of_week,
        start_time__date__lte=end_of_week,
    ).select_related('patient', 'provider')

    for appt in appointments:
        minutes_past_6am = (appt.start_time.hour - 6) * 60 + appt.start_time.minute
        appt.top_position = 64 + minutes_past_6am * (90 / 60)    # Scale minutes to the current 90px-per-hour ruler

    appointments_by_day = defaultdict(list)
    for appt in appointments:
        day = appt.start_time.date()
        appointments_by_day[day].append(appt)
        

    # * Adding a set of pre-made days ie. Monday to Sunday for the rendered final list
    week_days = [start_of_week + timedelta(days=i) for i in range(7)]
    schedule = [(day, appointments_by_day.get(day, [])) for day in week_days]

    hours = [f"{h}:00" for h in range(6, 22)]   # 6AM to 8PM, adjustable range (added 10 cause the... 
                                                # ...overflow hidden removes the last hour)
    

    stats = {
        'total': todays_appointments.count(),
        'completed': todays_appointments.filter(status='completed').count(),
        'upcoming': todays_appointments.filter(status='scheduled').count(),
        'no_show': todays_appointments.filter(status='no_show').count(),
    }

    context = {
        'active_page': 'calendar',
        'appointments': appointments,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'prev_week': start_of_week - timedelta(days=7),
        'next_week': start_of_week + timedelta(days=7),
        'is_current_week': is_current_week,
        'week_days': week_days,
        'today_display': today_display,
        'hours': hours,
        'schedule': schedule,
        'stats': stats,
    }
    return render(request, 'appointments/calendar.html', context, stats)




# ! PATIENTS PAGE VIEW
def patients_view(request):
    patients = Patient.objects.all()
    today = timezone.localdate()
    now = timezone.now()
    start_of_month = today.replace(day=1)


    for patient in patients:
        appointments = patient.appointment_set.all()
        patient.last_visit = appointments.filter(
            start_time__lt=timezone.now()
        ).order_by('-start_time').first()

        patient.upcoming_visit = appointments.filter(
            start_time__gte=timezone.now()
        ).order_by('start_time').first()

    active_patients = patients.filter(
        appointment__start_time__gte=now,
        appointment__status='scheduled',
    ).distinct()
    this_months_patients = patients.filter(
        created_at__date__gte=start_of_month,
    )


    context = {
        'patients' : patients,
        'active_patients_total' : active_patients.count(),
        'new_this_month' : this_months_patients.count(),
        'total_patients': patients.count(),
        'active_page': 'patients',
        }
    return render(request, 'appointments/patients.html', context)


# ! PROVIDERS PAGE VIEW
def providers_view(request):
    context = {
            'active_page': 'providers',
        }
    return render(request, 'appointments/providers.html', context)


# ! ANALYTICS PAGE VIEW
def analytics_view(request):
    context = {
            'active_page': 'analytics',
        }
    return render(request, 'appointments/analytics.html', context)


# ! PROFILE PAGE VIEW
def profile_view(request):
    context = {
            'active_page': 'profile',
        }
    return render(request, 'appointments/profile.html', context)





# -------------------------------------------------function views for features---------------------------------------------------------------
# ! Way to update an appointment's status
@require_POST
def update_appointment_status(request, appointment_id, new_status):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    appointment.status = new_status
    appointment.save()
    return redirect('calendar')


# ! View to dynamically search appointments and details from the search box
def search_appointments(request):
    query = request.GET.get('q', '')

    if len(query) < 2:
        return JsonResponse({'results': []})

    appointments = Appointment.objects.filter(
        Q(patient__name__icontains=query)   |
        Q(provider__name__icontains=query)
    ).select_related('patient', 'provider')[:8]

    results = []
    for appt in appointments:
        results.append({
            'id': appt.pk,
            'patient_name': appt.patient.name,
            'patient_age': appt.patient.age,
            'patient_condition': appt.patient.condition,
            'duration': appt.duration_minutes,
            'status': appt.status,            
            'provider_name': appt.provider.name,
            'appointment_type': appt.get_appointment_type_display(),
            'time': appt.start_time.strftime('%H:%M'),
        })

    return JsonResponse({'results': results})

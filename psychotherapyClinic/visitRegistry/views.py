from django.shortcuts import render,  get_object_or_404, redirect
from .models import Therapist, Patient, Visit, VisitDate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SymptomsForm, PatientForm, TherapistForm
from django.db.models import Q

def home(request):
    return render(request,'home.html')

def therapist_list(request):
    therapists = Therapist.objects.all()
    user_list = User.objects.all()
    return render(request, 'therapist_list.html',{'therapists':therapists,'user_list':user_list})

@login_required (login_url='login_user') 
def account(request):
    user = request.user
    if user.is_staff:
        additional_data = get_object_or_404(Therapist, user_id=user.id)
    else:
        additional_data = get_object_or_404(Patient, user_id=user.id)
    return render(request,'account.html',{'user': user,'additional_data': additional_data})

@login_required (login_url='login_user') 
def patient_symptoms_edit(request):
    user = request.user
    if request.method == 'GET':      
        patient = get_object_or_404(Patient, user_id=user.id)
        form = SymptomsForm(instance=patient)
        return render(request,'patient_symptoms_edit.html', {'form':form})
    else:
        patient = get_object_or_404(Patient, user_id=user.id)
        form = SymptomsForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            error = 'Something went wrong'
            return render(request, 'patien_symptoms_edit.html', {'form':form, 'error':error})
        
        
@login_required (login_url='login_user') 
def therapist_data_edit(request):
    user = request.user
    if request.method == 'GET':
        therapist = get_object_or_404(Therapist, user_id=user.id)
        form = TherapistForm(instance=therapist)
        return render(request,'therapist_data_edit.html', {'form':form})
    else:
        therapist = get_object_or_404(Therapist, user_id=user.id)
        form = TherapistForm(request.POST, instance=therapist)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            error = 'Something went wrong'
            return render(request, 'therapist_data_edit.html', {'form':form, 'error':error})
    
@login_required (login_url='login_user') 
def therapist_patient_edit(request, patient_user_id):
    patient_user = get_object_or_404(User, id=patient_user_id)
    patient = get_object_or_404(Patient, user_id=patient_user.id)
    if request.method == 'GET':
        form = PatientForm(instance=patient)
        visits = Visit.objects.filter(patient_id=patient.id)
        return render(request,'therapist_patient_edit.html', {'form':form, 'visits':visits, 'patient':patient_user})
    else:
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
        else:
            error = 'Something went wrong'
            return render(request, 'therapist_patient_edit.html', {'form':form, 'error':error})
        
@login_required (login_url='login_user') 
def patient_list(request):
    user = request.user
    therapist = get_object_or_404(Therapist, user_id=user.id)
    visits = Visit.objects.filter(therapist_id=therapist.id, is_confirmed=True)
    patients_list = visits.values('patient_id').distinct()
    patients = Patient.objects.filter(id__in=patients_list)
    patients_id_list = patients.values('user_id').distinct()
    user_list = User.objects.filter(id__in=patients_id_list)
    return render(request,'patient_list.html',{'user_list':user_list})

@login_required (login_url='login_user') 
def visit_list(request):
    user = request.user
    if user.is_staff:
        therapist = get_object_or_404(Therapist, user_id = user.id)
        visits= Visit.objects.filter(therapist_id=therapist.id).exclude(patient_id=None)
        visits_confirmed = visits.filter(is_confirmed=True)
        visits_confirmed_ids = visits_confirmed.values('visit_date_id').distinct()
        visit_confirmed_dates = VisitDate.objects.filter(id__in=visits_confirmed_ids)
        visits_not_confirmed = visits.filter(is_confirmed=False)
        visits_not_confirmed_ids = visits_not_confirmed.values('visit_date_id').distinct()
        visit_not_confirmed_dates = VisitDate.objects.filter(id__in=visits_not_confirmed_ids)
    else:
        patient = get_object_or_404(Patient, user_id = user.id)
        visits = Visit.objects.filter(patient_id=patient.id)
        visits_confirmed = visits.filter(is_confirmed=True)
        visits_confirmed_ids = visits_confirmed.values('visit_date_id').distinct()
        visit_confirmed_dates = VisitDate.objects.filter(id__in=visits_confirmed_ids)
        visits_not_confirmed = visits.filter(is_confirmed=False)
        visits_not_confirmed_ids = visits_not_confirmed.values('visit_date_id').distinct()
        visit_not_confirmed_dates = VisitDate.objects.filter(id__in=visits_not_confirmed_ids)
    return render(request,'visit_list.html',{'visits_confirmed': visit_confirmed_dates,'visits_not_confirmed': visit_not_confirmed_dates})

@login_required (login_url='login_user') 
def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, visit_date_id=visit_id)
    therapists = Therapist.objects.all()
    patients = Patient.objects.all()
    visit_dates = VisitDate.objects.all()
    user_list = User.objects.all()
    return render(request,'visit_detail.html',{'visit':visit,'therapists':therapists,'patients':patients,'visit_dates':visit_dates,'user_list':user_list})

@login_required (login_url='login_user') 
def therapist_schedule(request):
    if request.method == 'GET':
        user = request.user
        therapist = get_object_or_404(Therapist, user_id=user.id)
        working_hours = VisitDate.objects.all()
        reserved_hours = Visit.objects.filter(therapist_id=therapist.id)
        return render(request,'therapist_schedule.html',{'working_hours':working_hours, 'reserved_hours':reserved_hours, 'therapist_id':therapist.id})

@login_required (login_url='login_user')    
def confirm_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.is_confirmed= True
    visit.save()
    return redirect('visit_detail', visit_id=visit_id)

@login_required (login_url='login_user')
def visit_create_user(request):
    user = request.user
    patients = Patient.objects.values_list('user_id', flat=True)
    therapists = Therapist.objects.values_list('user_id', flat=True)
    if user.id in patients:
        return redirect ('choose_therapist')
    elif user.id in therapists:
        return redirect ('visit_create_therapist')
    else:
        return redirect('home')
    
@login_required (login_url='login_user')
def choose_therapist(request):
    user = request.user
    if request.method=='GET':
        therapists = Therapist.objects.all()
        thereapist_ids = therapists.values('user_id').distinct()
        therapist_user_list = User.objects.filter(id__in=thereapist_ids)
        return render(request, 'choose_therapist.html', {'therapists':therapists,'therapist_list':therapist_user_list})
    else:
        therapist_id = request.POST.get('therapist_select')
        return redirect('visit_create_patient', therapist_id=therapist_id)

@login_required (login_url='login_user')
def visit_create_patient(request, therapist_id):
    if request.method == 'GET':
        therapist_user = get_object_or_404(User, id=therapist_id)
        therapist = get_object_or_404(Therapist, user_id=therapist_id)
        visit_list = Visit.objects.filter(therapist_id=therapist.id)
        visit_dates = VisitDate.objects.filter(is_visit=False, is_reserved=True)
        visit_ids = visit_list.values('visit_date_id').distinct()
        reserved_visits = visit_dates.filter(id__in=visit_ids)
        user_list = User.objects.all()
        return render(request, 'visit_create_patient.html', {'therapist':therapist_user,'visits':reserved_visits,'user_list':user_list})

@login_required (login_url='login_user')
def visit_create_therapist(request):
    user = request.user
    if request.method == 'GET':
        therapist = get_object_or_404(Therapist, user_id=user.id)
        patient_ids = Patient.objects.values('user_id').distinct()
        patient_list = User.objects.filter(id__in=patient_ids)
        visit_list = Visit.objects.filter(therapist_id=therapist.id)
        visit_date_ids = visit_list.values('visit_date_id').distinct()
        visit_dates = VisitDate.objects.filter(Q(is_visit=False, is_reserved=False) | Q(id__in=visit_date_ids,is_reserved=True))
        return render(request, 'visit_create_therapist.html', {'visit_dates':visit_dates, 'patient_list':patient_list}) 

 
@login_required (login_url='login_user')
def create_visit_therapist(request):  
    user = request.user
    visit_date_id = request.POST.get('visit_date_select') 
    therapist = get_object_or_404(Therapist, user_id=user.id)
    patient_user_id = request.POST.get('patient_select')
    patient= get_object_or_404(Patient, user_id=patient_user_id)
    booked_by_patient = False
    is_confirmed = False     
    created_visit_date = get_object_or_404(VisitDate, id=visit_date_id)
    created_visit_date.is_visit = True
    created_visit_date.save()
    Visit.objects.create(visit_date_id=visit_date_id,patient_id=patient.id,therapist_id=therapist.id,booked_by_patient=booked_by_patient,is_confirmed=is_confirmed)
    return redirect('visit_list')

@login_required (login_url='login_user')
def create_visit_patient(request):  
    user = request.user
    visit_date_id = request.POST.get('visit_date_select') 
    patient = get_object_or_404(Patient, user_id=user.id)
    created_visit_date = get_object_or_404(VisitDate, id=visit_date_id)
    created_visit_date.is_visit = True
    created_visit_date.save()
    visit = get_object_or_404(Visit, visit_date_id = created_visit_date.id)
    visit.patient_id = patient.id
    visit.booked_by_patient = True
    visit.is_confirmed = False
    visit.save()
    return redirect('visit_list')

@login_required (login_url='login_user')
def cancel_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit_date = get_object_or_404(VisitDate, id = visit.visit_date_id)
    if visit_date.is_reserved:
        visit.patient_id = None
        visit.booked_by_patient = False
        visit.is_confirmed = False
        visit.save()
    else:
        visit.delete()
    visit_date.is_visit = False
    visit_date.save()
    return redirect('visit_list')

@login_required (login_url='login_user')
def visit_reserve_therapist(request):
    user  = request.user
    if request.method == 'GET':
        therapist = get_object_or_404(Therapist, user_id=user.id)
        visit_dates = VisitDate.objects.filter(is_visit=False, is_reserved=False)
        user_list = User.objects.all()
        return render(request, 'visit_reserve_therapist.html', {'therapist':therapist,'visit_dates':visit_dates, 'user_list':user_list}) 
    else:
        reserved_visit_date_id = request.POST.get('visit_date_select') 
        reserved_visit_date = get_object_or_404(VisitDate, id=reserved_visit_date_id)
        reserved_visit_date.is_reserved=True
        therapist = get_object_or_404(Therapist, user_id=user.id)
        Visit.objects.create(visit_date_id=reserved_visit_date_id,patient_id=None,therapist_id=therapist.id,booked_by_patient=False,is_confirmed=False)
        reserved_visit_date.save()
        return redirect('therapist_schedule')
    
@login_required (login_url='login_user')
def cancel_reserved(request):
    user = request.user
    if request.method == 'GET': 
        therapist = get_object_or_404(Therapist, user_id=user.id)
        reservations = Visit.objects.filter(therapist_id=therapist.id, patient_id=None)
        visit_dates = VisitDate.objects.filter(is_reserved=True, is_visit=False)
        return render(request, 'cancel_reserved.html', {'reserved':reservations,'visit_dates':visit_dates})
    else:
        cancelled_date_id = request.POST.get('reserved_select')
        cancelled_visit = get_object_or_404(Visit, id=cancelled_date_id)
        visit_date = get_object_or_404(VisitDate, id=cancelled_visit.visit_date_id)
        visit_date.is_reserved = False
        visit_date.save()
        cancelled_visit.delete()
        return redirect('therapist_schedule')
    


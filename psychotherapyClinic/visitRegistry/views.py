from django.shortcuts import render,  get_object_or_404, redirect
from .models import Therapist, Patient, Visit, Visit_date
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

@login_required (login_url='login_user') 
def account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        additional_data = get_object_or_404(Therapist, user_id=user_id)
    else:
        additional_data = get_object_or_404(Patient, user_id=user_id)
    return render(request,'account.html',{'user': user,'additional_data': additional_data})

@login_required (login_url='login_user') 
def visit_list(request):
    visits = Visit.objects.all()
    visit_hours = Visit_date.objects.all()
    return render(request,'visit_list.html',{'visits': visits,'visit_hours':visit_hours})

@login_required (login_url='login_user') 
def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    therapists = Therapist.objects.all()
    patients = Patient.objects.all()
    visit_dates = Visit_date.objects.all()
    user_list = User.objects.all()
    return render(request,'visit_detail.html',{'visit':visit,'therapists':therapists,'patients':patients,'visit_dates':visit_dates,'user_list':user_list})

@login_required (login_url='login_user') 
def therapist_schedule(request,therapist_id):
    if request.method == 'GET':
        working_hours = Visit_date.objects.all()
        reserved_hours = Visit.objects.filter(therapist_id=therapist_id)
        return render(request,'therapist_schedule.html',{'working_hours':working_hours, 'reserved_hours':reserved_hours, 'therapist_id':therapist_id})

@login_required (login_url='login_user')    
def confirm_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.is_confirmed= True
    visit.save()
    return redirect('visit_detail', visit_id=visit_id)

@login_required (login_url='login_user')
def visit_create_user(request, user_id):
    patients = Patient.objects.values_list('user_id', flat=True)
    therapists = Therapist.objects.values_list('user_id', flat=True)
    if user_id in patients:
        return redirect ('visit_create_patient', user_id=user_id)
    elif user_id in therapists:
        return redirect ('visit_create_therapist', user_id=user_id)
    else:
        return redirect('home')

@login_required (login_url='login_user')
def visit_create_patient(request, user_id):
    if request.method == 'GET':
        patient = get_object_or_404(Patient, user_id=user_id)
        therapists = Therapist.objects.all()
        visit_list = Visit.objects.all()
        visit_dates = Visit_date.objects.all()
        user_list = User.objects.all()
        return render(request, 'visit_create_patient.html', {'patient':patient,'therapists':therapists,'visit_list':visit_list,'visit_dates':visit_dates,'user_list':user_list})

@login_required (login_url='login_user')
def visit_create_therapist(request, user_id):
    if request.method == 'GET':
        therapist = get_object_or_404(Therapist, user_id=user_id)
        patients = Patient.objects.all()
        visit_list = Visit.objects.all()
        visit_dates = Visit_date.objects.all()
        user_list = User.objects.all()
        return render(request, 'visit_create_therapist.html', {'patients':patients,'therapist':therapist,'visit_list':visit_list,'visit_dates':visit_dates, 'user_list':user_list}) 

 
@login_required (login_url='login_user')
def create_visit(request, user_id):  
    visit_date_id = request.POST.get('visit_date_select') 
    if request.method == 'POST':
        if Patient.objects.filter(user_id=user_id):
            patient = get_object_or_404(Patient, user_id=user_id)
            patient_id = patient.id
            therapist_id = request.POST.get('therapist_select')
            booked_by_patient = True
            is_confirmed = False
        else:
            therapist = get_object_or_404(Therapist, user_id=user_id)
            therapist_id = therapist.id
            patient_id = request.POST.get('patient_select')
            booked_by_patient = False
            is_confirmed = False
       
        Visit.objects.create(visit_date_id=visit_date_id,patient_id=patient_id,therapist_id=therapist_id,booked_by_patient=booked_by_patient,is_confirmed=is_confirmed)
        return redirect('visit_list')

@login_required (login_url='login_user')
def cancel_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.delete()
    return redirect('visit_list')
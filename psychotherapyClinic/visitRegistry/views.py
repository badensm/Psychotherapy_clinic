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
    
def confirm_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    visit.is_confirmed = True
    visit.save()
    return redirect('visit_detail', visit_id=visit_id)
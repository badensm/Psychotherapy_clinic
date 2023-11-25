from django.shortcuts import render,  get_object_or_404
from .models import Therapist, Patient, Visit
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
    return render(request,'account.html',{'user': user, 'additional_data': additional_data})

@login_required (login_url='login_user') 
def visit_list(request):
    visits = Visit.objects.all()
    return render(request,'visit_list.html',{'visits': visits})

@login_required (login_url='login_user') 
def visit_detail(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    return render(request,'visit_detail.html')
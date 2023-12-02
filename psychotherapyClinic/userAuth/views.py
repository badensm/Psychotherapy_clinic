from django.forms import ValidationError
from django.shortcuts import redirect, render
from .forms import RegisterForm, EditForm
from django.contrib.auth.models import User
from .utils import check_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from visitRegistry.models import Therapist, Patient

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            username_taken = User.objects.filter(username=username).exists()
            email_taken = User.objects.filter(email=email).exists()

            if username_taken:
                error = 'Ten login jest zajęty. Spróbuj jeszcze raz.'
            elif email_taken:
                error = 'Ten e-mail jest zajęty. Spróbuj jeszcze raz.' 
            else:
                email_valid = check_email(email)  
                if email_valid:
                    try:
                        validate_password(password1)
                    except ValidationError as e:
                        return render(request, 'register.html', {'password_errors': e.messages, 'form': RegisterForm()})
                    else:
                        is_therapist = False
                        if is_staff == "on":
                            is_therapist = True
                        user = User.objects.create_user(first_name=first_name,last_name=last_name,is_staff=is_therapist,username=username,email=email,password=password1)
                        if is_staff:
                            therapist = Therapist.objects.create(user_id=user.id,visit_rate=0)
                        else:
                            patient = Patient.objects.create(user_id=user.id)
                        return redirect('home')

                else:
                    error = 'Niewłaściwy e-mail. Spróbuj jeszcze raz.'  
        else:
            error = 'Hasła nie są zgodne. Spróbuj jeszcze raz!'

    return render(request, 'register.html',{'form':RegisterForm(), 'error': error})

def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': AuthenticationForm()})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                error = 'Niewłaściwe hasło'
            else:
                error = f'Użytkownik {username} nie istnieje'
            return render(request, 'login_user.html', {'form': AuthenticationForm(),'error':error})

@login_required(login_url='login_user')        
def logout_user(request):
        logout(request)
        return redirect('home')

@login_required(login_url='login_user')  
def account_data_edit(request):
    if request.method == 'GET':
        form = EditForm(instance=request.user)
        return render(request, 'account_data_edit.html', {'form': form})
    else:
        form = EditForm(instance=request.user)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
      
        email_taken = User.objects.filter(email=email).exists()

        if email_taken:
            error = 'Ten e-mail jest zajęty. Spróbuj jeszcze raz.' 
        else:
            email_valid = check_email(email)  
            if email_valid:
                    user = request.user
                    user.first_name=first_name
                    user.last_name=last_name
                    user.email=email
                    user.save()
                    return redirect('account', user_id=user.id)

            else:
                error = 'Niewłaściwy e-mail. Spróbuj jeszcze raz.'  


    return render(request, 'account_data_edit.html',{'form':form, 'error': error})
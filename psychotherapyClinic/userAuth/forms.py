from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff', 'username', 'email', 'password1', 'password2')
        labels = {
            'first_name': "Imię:",
            'last_name': "Nazwisko:",
            'is_staff': "Jestem terapeutą",
            'username':"Login:",
            'email': "Adres e-mail:",
            'password1':"Hasło:",
            'password2':"Powtórz hasło"
        }
        

class EditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': "Imię:",
            'last_name': "Nazwisko:",
            'email': "Adres e-mail:"
        }

    

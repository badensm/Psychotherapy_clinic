from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff', 'username', 'email', 'password1', 'password2')
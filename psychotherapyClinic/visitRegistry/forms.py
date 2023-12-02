from .models import Patient, Therapist
from django.forms import ModelForm

class SymptomsForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('symptoms',)
        labels = {'symptoms': "Twoje objawy"}

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ('diagnosis','symptoms')
        labels = {'diagnosis':"Diagnoza",'symptoms': "Objawy"}

class TherapistForm(ModelForm):
    class Meta:
        model = Therapist
        fields = ('visit_rate','info')
        labels = {'visit_rate':"Stawka godzinowa", 'info': "Informacje"}

    

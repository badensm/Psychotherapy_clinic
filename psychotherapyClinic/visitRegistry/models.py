from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Therapist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_rate = models.FloatField()
    info = models.TextField(blank=True)

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=200,blank=True)
    symptoms = models.TextField(blank=True)

class Visit_date(models.Model):
    day = models.PositiveSmallIntegerField()
    hours = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.day} | {self.hours}'

class Visit(models.Model):
    visit_date = models.ForeignKey(Visit_date, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    
    


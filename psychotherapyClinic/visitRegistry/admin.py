from django.contrib import admin
from .models import Therapist, Patient, VisitDate, Visit

# Register your models here.
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(VisitDate)
admin.site.register(Visit)

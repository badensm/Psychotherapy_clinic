from django.contrib import admin
from .models import Therapist, Patient, Visit_date, Visit

# Register your models here.
admin.site.register(Therapist)
admin.site.register(Patient)
admin.site.register(Visit_date)
admin.site.register(Visit)
